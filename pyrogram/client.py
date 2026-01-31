from __future__ import annotations

import asyncio
import contextlib
import functools
import inspect
import logging
import os
import platform
import re
import shutil
import sys
from collections import OrderedDict
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from hashlib import sha256
from pathlib import Path
from typing import TYPE_CHECKING, Any

from pyrogram import __license__, __version__, raw, utils
from pyrogram.crypto import aes
from pyrogram.errors import (
    BadRequest,
    CDNFileHashMismatch,
    ChannelPrivate,
    FloodPremiumWait,
    FloodWait,
    PeerIdInvalid,
    SessionPasswordNeeded,
    VolumeLocNotFound,
)
from pyrogram.handlers.handler import Handler
from pyrogram.session import Auth, Session
from pyrogram.storage import FileStorage, MemoryStorage, Storage
from pyrogram.utils import ainput

from .connection import Connection
from .connection.transport import TCP, TCPAbridged
from .dispatcher import Dispatcher
from .session.internals import MsgId

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Callable
    from pyrogram.raw.core import TLObject

log = logging.getLogger(__name__)


class Client:
    """Pyrogram Client, the main means for interacting with Telegram.
    """

    APP_VERSION = f"Electrogram {__version__}"
    DEVICE_MODEL = f"{platform.python_implementation()} {platform.python_version()}"
    SYSTEM_VERSION = f"{platform.system()} {platform.release()}"

    LANG_CODE = "en"
    SYSTEM_LANG_CODE = "en-US"
    LANG_PACK = ""

    PARENT_DIR = Path(sys.argv[0]).parent

    INVITE_LINK_RE = re.compile(
        r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:joinchat/|\+))([\w-]+)$",
    )
    WORKERS = min(64, (os.cpu_count() or 0) + 4)
    WORKDIR = PARENT_DIR
    UPDATES_WATCHDOG_INTERVAL = 10 * 60
    MAX_CONCURRENT_TRANSMISSIONS = 1000
    MAX_MESSAGE_CACHE_SIZE = 10000

    def __init__(
        self,
        name: str,
        api_id: int | str | None = None,
        api_hash: str | None = None,
        app_version: str = APP_VERSION,
        device_model: str = DEVICE_MODEL,
        system_version: str = SYSTEM_VERSION,
        lang_code: str = LANG_CODE,
        system_lang_code: str = SYSTEM_LANG_CODE,
        lang_pack: str = LANG_PACK,
        ipv6: bool = False,
        alt_port: bool = False,
        proxy: dict | None = None,
        test_mode: bool = False,
        bot_token: str | None = None,
        session_string: str | None = None,
        is_telethon_string: bool = False,
        in_memory: bool | None = None,
        storage: Storage = None,
        phone_number: str | None = None,
        phone_code: str | None = None,
        password: str | None = None,
        workers: int = WORKERS,
        workdir: str = WORKDIR,
        plugins: dict | None = None,
        no_updates: bool | None = None,
        skip_updates: bool = True,
        takeout: bool | None = None,
        sleep_threshold: int = Session.SLEEP_THRESHOLD,
        hide_password: bool = False,
        max_concurrent_transmissions: int = MAX_CONCURRENT_TRANSMISSIONS,
        init_params: raw.types.JsonObject = None,
        max_message_cache_size: int = MAX_MESSAGE_CACHE_SIZE,
        connection_factory: type[Connection] = Connection,
        protocol_factory: type[TCP] = TCPAbridged,
    ) -> None:
        self.name = name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code.lower()
        self.system_lang_code = system_lang_code
        self.lang_pack = lang_pack.lower()
        self.ipv6 = ipv6
        self.alt_port = alt_port
        self.proxy = proxy
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.session_string = session_string
        self.is_telethon_string = is_telethon_string
        self.in_memory = in_memory
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.workers = workers
        self.workdir = Path(workdir)
        self.plugins = plugins
        self.no_updates = no_updates
        self.skip_updates = skip_updates
        self.takeout = takeout
        self.sleep_threshold = sleep_threshold
        self.hide_password = hide_password
        self.max_concurrent_transmissions = max_concurrent_transmissions
        self.init_params = init_params
        self.max_message_cache_size = max_message_cache_size
        self.connection_factory = connection_factory
        self.protocol_factory = protocol_factory

        self.executor = ThreadPoolExecutor(
            self.workers,
            thread_name_prefix="Handler",
        )

        if storage:
            self.storage = storage
        elif self.session_string:
            self.storage = MemoryStorage(
                self.name,
                self.session_string,
                self.is_telethon_string,
            )
        elif self.in_memory:
            self.storage = MemoryStorage(self.name)
        else:
            self.storage = FileStorage(self.name, self.workdir)
        self.dispatcher = Dispatcher(self)
        self.rnd_id = MsgId
        self.session = None
        self.media_sessions = {}
        self.media_sessions_lock = asyncio.Lock()
        self.save_file_semaphore = asyncio.Semaphore(
            self.max_concurrent_transmissions,
        )
        self.get_file_semaphore = asyncio.Semaphore(
            self.max_concurrent_transmissions,
        )
        self.is_connected = None
        self.is_initialized = None
        self.takeout_id = None
        self.disconnect_handler = None
        self.me: raw.types.User | None = None
        self.message_cache = Cache(self.max_message_cache_size)
        self.updates_watchdog_task = None
        self.updates_watchdog_event = asyncio.Event()
        self.updates_invoke_error = None
        self.last_update_time = datetime.now()
        self.loop = asyncio.get_event_loop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        with contextlib.suppress(ConnectionError):
            self.stop()

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        with contextlib.suppress(ConnectionError):
            await self.stop()

    async def invoke(
        self,
        query: TLObject,
        retries: int = Session.MAX_RETRIES,
        timeout: float = Session.WAIT_TIMEOUT,
        sleep_threshold: float | None = None,
    ):
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if self.no_updates:
            query = raw.functions.InvokeWithoutUpdates(query=query)

        if self.takeout_id:
            query = raw.functions.InvokeWithTakeout(
                takeout_id=self.takeout_id,
                query=query,
            )

        r = await self.session.invoke(
            query,
            retries,
            timeout,
            (
                sleep_threshold
                if sleep_threshold is not None
                else self.sleep_threshold
            ),
        )

        await self.fetch_peers(getattr(r, "users", []))
        await self.fetch_peers(getattr(r, "chats", []))

        return r

    async def resolve_peer(
        self,
        peer_id: int | str,
    ) -> raw.base.InputPeer | raw.base.InputUser | raw.base.InputChannel:
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if peer_id in ("self", "me"):
            return raw.types.InputPeerSelf()
        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())
                peer_id = re.sub(r"https://t.me/", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.invoke(
                            raw.functions.contacts.ResolveUsername(username=peer_id),
                        )

                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid from None

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                await self.fetch_peers(
                    await self.invoke(
                        raw.functions.users.GetUsers(
                            id=[raw.types.InputUser(user_id=peer_id, access_hash=0)],
                        ),
                    ),
                )
            elif peer_type == "chat":
                await self.invoke(raw.functions.messages.GetChats(id=[-peer_id]))
            else:
                await self.invoke(
                    raw.functions.channels.GetChannels(
                        id=[
                            raw.types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id),
                                access_hash=0,
                            ),
                        ],
                    ),
                )

            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid from None

    async def start(self) -> Client:
        await self.load_session()
        self.session = Session(
            self,
            await self.storage.dc_id(),
            await self.storage.auth_key(),
            await self.storage.test_mode(),
        )

        await self.session.start()
        self.is_connected = True

        try:
            if not await self.storage.is_bot() and self.takeout:
                takeout = await self.invoke(raw.functions.account.InitTakeoutSession())
                self.takeout_id = takeout.id
                log.info("Takeout session %s initialized", self.takeout_id)

            await self.dispatcher.start()

            if not await self.storage.user_id():
                self.me = await self.authorize()
                await self.storage.user_id(self.me.id)
                await self.storage.is_bot(self.me.bot)
            else:
                self.me = raw.types.User(
                    id=await self.storage.user_id(),
                    is_self=True,
                    bot=await self.storage.is_bot(),
                )

            self.updates_watchdog_task = self.loop.create_task(self.updates_watchdog())

            log.info("Client started")
        except Exception:
            await self.stop()
            raise

        return self

    async def stop(self, block: bool = True) -> None:
        if not self.is_connected:
            raise ConnectionError("Client is already stopped")

        if self.updates_watchdog_task:
            self.updates_watchdog_task.cancel()

        await self.dispatcher.stop()
        await self.session.stop()
        await self.storage.close()

        self.is_connected = False
        log.info("Client stopped")

    async def updates_watchdog(self) -> None:
        while True:
            try:
                await asyncio.wait_for(
                    self.updates_watchdog_event.wait(),
                    self.UPDATES_WATCHDOG_INTERVAL,
                )
            except asyncio.TimeoutError:
                pass
            else:
                break

            if datetime.now() - self.last_update_time > timedelta(
                seconds=self.UPDATES_WATCHDOG_INTERVAL,
            ):
                with contextlib.suppress(Exception):
                    await self.invoke(raw.functions.updates.GetState())

    async def authorize(self) -> raw.types.User:
        if self.bot_token:
            return await self.invoke(raw.functions.auth.SignInBot(
                bot_token=self.bot_token,
                api_id=self.api_id,
                api_hash=self.api_hash
            ))

        print(f"Welcome to Pyrogram (version {__version__})")
        print(
            f"Pyrogram is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n"
            f"under the terms of the {__license__}.\n",
        )

        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = await ainput("Enter phone number or bot token: ")

                        if not value:
                            continue

                        confirm = (
                            await ainput(f'Is "{value}" correct? (y/N): ')
                        ).lower()

                        if confirm == "y":
                            break

                    if ":" in value:
                        self.bot_token = value
                        return await self.invoke(raw.functions.auth.SignInBot(
                            bot_token=value,
                            api_id=self.api_id,
                            api_hash=self.api_hash
                        ))
                    self.phone_number = value

                sent_code = await self.invoke(raw.functions.auth.SendCode(
                    phone_number=self.phone_number.strip(" +"),
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    settings=raw.types.CodeSettings()
                ))
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        print("The confirmation code has been sent")

        while True:
            if not self.phone_code:
                self.phone_code = await ainput("Enter confirmation code: ")

            try:
                signed_in = await self.invoke(raw.functions.auth.SignIn(
                    phone_number=self.phone_number,
                    phone_code_hash=sent_code.phone_code_hash,
                    phone_code=self.phone_code
                ))
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded:
                while True:
                    password_res = await self.invoke(raw.functions.account.GetPassword())
                    print(f"Password hint: {password_res.hint}")

                    if not self.password:
                        self.password = await ainput(
                            "Enter password (empty to recover): ",
                            hide=self.hide_password,
                        )

                    try:
                        if not self.password:
                            confirm = await ainput(
                                "Confirm password recovery (y/n): ",
                            )

                            if confirm == "y":
                                email_pattern = (await self.invoke(raw.functions.auth.RequestPasswordRecovery())).email_pattern
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await ainput("Enter recovery code: ")

                                    try:
                                        signed_in = await self.invoke(raw.functions.auth.RecoverPassword(
                                            code=recovery_code
                                        ))
                                        return signed_in.user
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                            else:
                                self.password = None
                        else:
                            signed_in = await self.invoke(raw.functions.auth.CheckPassword(
                                password=utils.compute_password_check(password_res, self.password)
                            ))
                            return signed_in.user
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, raw.types.auth.Authorization):
            return signed_in.user

        if isinstance(signed_in, raw.types.auth.AuthorizationSignUpRequired):
            while True:
                first_name = await ainput("Enter first name: ")
                last_name = await ainput("Enter last name (empty to skip): ")

                try:
                    signed_up = await self.invoke(raw.functions.auth.SignUp(
                        phone_number=self.phone_number,
                        phone_code_hash=sent_code.phone_code_hash,
                        first_name=first_name,
                        last_name=last_name
                    ))
                    return signed_up.user
                except BadRequest as e:
                    print(e.MESSAGE)

        return signed_in

    async def fetch_peers(
        self,
        peers: list[raw.types.User | raw.types.Chat | raw.types.Channel],
    ) -> bool:
        is_min = False
        parsed_peers = []
        usernames = []

        for peer in peers:
            if getattr(peer, "min", False):
                is_min = True
                continue

            username = None
            phone_number = None

            if isinstance(peer, raw.types.User):
                peer_id = peer.id
                access_hash = peer.access_hash
                username = (
                    peer.username.lower()
                    if peer.username
                    else peer.usernames[0].username.lower()
                    if peer.usernames
                    else None
                )
                if peer.usernames is not None and len(peer.usernames) > 1:
                    usernames.extend(
                        (peer.id, uname.username.lower()) for uname in peer.usernames
                    )
                phone_number = peer.phone
                peer_type = "bot" if peer.bot else "user"
            elif isinstance(peer, (raw.types.Chat, raw.types.ChatForbidden)):
                peer_id = -peer.id
                access_hash = 0
                peer_type = "group"
            elif isinstance(peer, raw.types.Channel):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                username = (
                    peer.username.lower()
                    if peer.username
                    else peer.usernames[0].username.lower()
                    if peer.usernames
                    else None
                )
                if peer.usernames is not None and len(peer.usernames) > 1:
                    usernames.extend(
                        (peer.id, uname.username.lower()) for uname in peer.usernames
                    )
                peer_type = "channel" if peer.broadcast else "supergroup"
            elif isinstance(peer, raw.types.ChannelForbidden):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                peer_type = "channel" if peer.broadcast else "supergroup"
            else:
                continue

            parsed_peers.append(
                (peer_id, access_hash, peer_type, username, phone_number),
            )

        await self.storage.update_peers(parsed_peers)
        await self.storage.update_usernames(usernames)

        return is_min

    async def handle_updates(self, updates) -> None:
        self.last_update_time = datetime.now()

        if isinstance(updates, (raw.types.Updates, raw.types.UpdatesCombined)):
            await self.fetch_peers(updates.users)
            await self.fetch_peers(updates.chats)

            users = {u.id: u for u in updates.users}
            chats = {c.id: c for c in updates.chats}

            for update in updates.updates:
                channel_id = getattr(
                    getattr(getattr(update, "message", None), "peer_id", None),
                    "channel_id",
                    None,
                ) or getattr(update, "channel_id", None)

                pts = getattr(update, "pts", None)
                pts_count = getattr(update, "pts_count", None)

                if pts and not self.skip_updates:
                    await self.storage.update_state(
                        (
                            utils.get_channel_id(channel_id) if channel_id else 0,
                            pts,
                            None,
                            updates.date,
                            updates.seq,
                        ),
                    )
                self.dispatcher.updates_queue.put_nowait((update, users, chats))
        elif isinstance(
            updates,
            (raw.types.UpdateShortMessage, raw.types.UpdateShortChatMessage),
        ):
            if not self.skip_updates:
                await self.storage.update_state(
                    (0, updates.pts, None, updates.date, None),
                )
            self.dispatcher.updates_queue.put_nowait((updates, {}, {}))
        elif isinstance(updates, raw.types.UpdateShort):
            self.dispatcher.updates_queue.put_nowait((updates.update, {}, {}))

    async def load_session(self) -> None:
        await self.storage.open()

        session_empty = any(
            [
                await self.storage.test_mode() is None,
                await self.storage.auth_key() is None,
                await self.storage.user_id() is None,
                await self.storage.is_bot() is None,
            ],
        )

        if session_empty:
            if not self.api_id or not self.api_hash:
                raise AttributeError(
                    "The API key is required for new authorizations.",
                )

            await self.storage.api_id(self.api_id)

            await self.storage.dc_id(2)
            await self.storage.date(0)

            await self.storage.test_mode(self.test_mode)
            await self.storage.auth_key(
                await Auth(
                    self,
                    await self.storage.dc_id(),
                    await self.storage.test_mode(),
                ).create(),
            )
            await self.storage.user_id(None)
            await self.storage.is_bot(None)

    def add_handler(self, handler: Handler, group: int = 0):
        self.dispatcher.add_handler(handler, group)

    def remove_handler(self, handler: Handler, group: int = 0):
        self.dispatcher.remove_handler(handler, group)

    def on_raw_update(self, group: int = 0):
        def decorator(func: Callable) -> Callable:
            self.add_handler(pyrogram.handlers.RawUpdateHandler(func), group)
            return func

        return decorator


class Cache:
    def __init__(self, capacity: int) -> None:
        self.capacity = capacity
        self.store = OrderedDict()

    def __getitem__(self, key):
        value = self.store.pop(key, None)
        if value is not None:
            # Reinsert the accessed item as the most recent one
            self.store[key] = value
        return value

    def __setitem__(self, key, value) -> None:
        if key in self.store:
            del self.store[key]

        self.store[key] = value

        if len(self.store) > self.capacity:
            self.store.popitem(last=False)
