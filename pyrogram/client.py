from asyncio import Semaphore, Lock, Event, CancelledError, TimeoutError, get_event_loop, wait_for
from collections import OrderedDict
from functools import partial
from inspect import iscoroutinefunction
from logging import getLogger
from os import cpu_count, makedirs, path, remove
from platform import python_implementation, python_version, system, release
from re import compile, sub
from shutil import move
from sys import argv
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timedelta
from functools import lru_cache
from hashlib import sha256
from importlib import import_module
from io import StringIO, BytesIO
from mimetypes import MimeTypes
from pathlib import Path
from typing import Union, List, Optional, Callable, AsyncGenerator, Type

import pyrogram
from pyrogram import __version__, __license__
from pyrogram import enums
from pyrogram import raw
from pyrogram import utils
from pyrogram.crypto import aes
from pyrogram.errors import CDNFileHashMismatch
from pyrogram.errors import (
    SessionPasswordNeeded,
    VolumeLocNotFound,
    ChannelPrivate,
    BadRequest,
    FloodWait,
    FloodPremiumWait,
)
from pyrogram.handlers.handler import Handler
from pyrogram.methods import Methods
from pyrogram.session import Auth, Session
from pyrogram.storage import FileStorage, MemoryStorage, Storage
from pyrogram.types import User, TermsOfService
from pyrogram.utils import ainput
from .connection import Connection
from .connection.transport import TCP, TCPAbridged
from .dispatcher import Dispatcher
from .file_id import FileId, FileType, ThumbnailSource
from .mime_types import mime_types
from .parser import Parser
from .session.internals import MsgId

log = getLogger(__name__)


class Client(Methods):
    APP_VERSION = f"NekoZee {__version__}"
    DEVICE_MODEL = f"{python_implementation()} {python_version()}"
    SYSTEM_VERSION = f"{system()} {release()}"

    LANG_CODE = "en"
    SYSTEM_LANG_CODE = "en-US"
    LANG_PACK = ""

    PARENT_DIR = Path(argv[0]).parent

    INVITE_LINK_RE = compile(
        r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:joinchat/|\+))([\w-]+)$"
    )
    WORKERS = min(64, (cpu_count() or 0) + 4)
    WORKDIR = PARENT_DIR
    UPDATES_WATCHDOG_INTERVAL = 10 * 60
    MAX_CONCURRENT_TRANSMISSIONS = 1000
    MAX_MESSAGE_CACHE_SIZE = 10000
    mimetypes = MimeTypes()
    mimetypes.readfp(StringIO(mime_types))

    def __init__(
        self,
        name: str,
        api_id: Union[int, str] = None,
        api_hash: str = None,
        app_version: str = APP_VERSION,
        device_model: str = DEVICE_MODEL,
        system_version: str = SYSTEM_VERSION,
        lang_code: str = LANG_CODE,
        system_lang_code: str = SYSTEM_LANG_CODE,
        lang_pack: str = LANG_PACK,
        ipv6: bool = False,
        alt_port: bool = False,
        proxy: dict = None,
        test_mode: bool = False,
        bot_token: str = None,
        session_string: str = None,
        is_telethon_string: bool = False,
        in_memory: bool = None,
        storage: Storage = None,
        phone_number: str = None,
        phone_code: str = None,
        password: str = None,
        workers: int = WORKERS,
        workdir: str = WORKDIR,
        plugins: dict = None,
        parse_mode: "enums.ParseMode" = enums.ParseMode.DEFAULT,
        no_updates: bool = None,
        skip_updates: bool = True,
        takeout: bool = None,
        sleep_threshold: int = Session.SLEEP_THRESHOLD,
        hide_password: bool = False,
        max_concurrent_transmissions: int = MAX_CONCURRENT_TRANSMISSIONS,
        init_params: raw.types.JsonObject = None,
        max_message_cache_size: int = MAX_MESSAGE_CACHE_SIZE,
        client_platform: "enums.ClientPlatform" = enums.ClientPlatform.OTHER,
        connection_factory: Type[Connection] = Connection,
        protocol_factory: Type[TCP] = TCPAbridged,
    ):
        super().__init__()

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
        self.parse_mode = parse_mode
        self.no_updates = no_updates
        self.skip_updates = skip_updates
        self.takeout = takeout
        self.sleep_threshold = sleep_threshold
        self.hide_password = hide_password
        self.max_concurrent_transmissions = max_concurrent_transmissions
        self.init_params = init_params
        self.max_message_cache_size = max_message_cache_size
        self.client_platform = client_platform
        self.connection_factory = connection_factory
        self.protocol_factory = protocol_factory

        self.executor = ThreadPoolExecutor(self.workers, thread_name_prefix="Handler")

        if storage:
            self.storage = storage
        elif self.session_string:
            self.storage = MemoryStorage(
                self.name, self.session_string, self.is_telethon_string
            )
        elif self.in_memory:
            self.storage = MemoryStorage(self.name)
        else:
            self.storage = FileStorage(self.name, self.workdir)
        self.dispatcher = Dispatcher(self)
        self.rnd_id = MsgId
        self.parser = Parser(self)
        self.session = None
        self.media_sessions = {}
        self.media_sessions_lock = Lock()
        self.save_file_semaphore = Semaphore(self.max_concurrent_transmissions)
        self.get_file_semaphore = Semaphore(self.max_concurrent_transmissions)
        self.is_connected = None
        self.is_initialized = None
        self.takeout_id = None
        self.disconnect_handler = None
        self.me: Optional[User] = None
        self.message_cache = Cache(self.max_message_cache_size)
        self.updates_watchdog_task = None
        self.updates_watchdog_event = Event()
        self.updates_invoke_error = None
        self.last_update_time = datetime.now()
        self.listeners = {
            listener_type: [] for listener_type in pyrogram.enums.ListenerTypes
        }
        self.loop = get_event_loop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        try:
            self.stop()
        except ConnectionError:
            pass

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        try:
            await self.stop()
        except ConnectionError:
            pass

    async def updates_watchdog(self):
        while True:
            try:
                await wait_for(
                    self.updates_watchdog_event.wait(), self.UPDATES_WATCHDOG_INTERVAL
                )
            except TimeoutError:
                pass
            else:
                break

            if datetime.now() - self.last_update_time > timedelta(
                seconds=self.UPDATES_WATCHDOG_INTERVAL
            ):
                await self.invoke(raw.functions.updates.GetState())

    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        print(f"Welcome to nekozee (version {__version__})")
        print(
            f"nekozee is free software and comes with ABSOLUTELY NO WARRANTY. Licensed\n"
            f"under the terms of the {__license__}.\n"
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
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = await self.send_code(self.phone_number)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        sent_code_descriptions = {
            enums.SentCodeType.APP: "Telegram app",
            enums.SentCodeType.SMS: "SMS",
            enums.SentCodeType.CALL: "phone call",
            enums.SentCodeType.FLASH_CALL: "phone flash call",
            enums.SentCodeType.FRAGMENT_SMS: "Fragment SMS",
            enums.SentCodeType.EMAIL_CODE: "email code",
        }

        print(
            f"The confirmation code has been sent via {sent_code_descriptions[sent_code.type]}"
        )

        while True:
            if not self.phone_code:
                self.phone_code = await ainput("Enter confirmation code: ")

            try:
                signed_in = await self.sign_in(
                    self.phone_number, sent_code.phone_code_hash, self.phone_code
                )
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await ainput(
                            "Enter password (empty to recover): ",
                            hide=self.hide_password,
                        )

                    try:
                        if not self.password:
                            confirm = await ainput("Confirm password recovery (y/n): ")

                            if confirm == "y":
                                email_pattern = await self.send_recovery_code()
                                print(
                                    f"The recovery code has been sent to {email_pattern}"
                                )

                                while True:
                                    recovery_code = await ainput(
                                        "Enter recovery code: "
                                    )

                                    try:
                                        return await self.recover_password(
                                            recovery_code
                                        )
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        log.exception(e)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, User):
            return signed_in

        while True:
            first_name = await ainput("Enter first name: ")
            last_name = await ainput("Enter last name (empty to skip): ")

            try:
                signed_up = await self.sign_up(
                    self.phone_number, sent_code.phone_code_hash, first_name, last_name
                )
            except BadRequest as e:
                print(e.MESSAGE)
            else:
                break

        if isinstance(signed_in, TermsOfService):
            print("\n" + signed_in.text + "\n")
            await self.accept_terms_of_service(signed_in.id)

        return signed_up

    def set_parse_mode(self, parse_mode: Optional["enums.ParseMode"]):
        self.parse_mode = parse_mode

    async def fetch_peers(
        self, peers: List[Union[raw.types.User, raw.types.Chat, raw.types.Channel]]
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
                    else peer.usernames[0].username.lower() if peer.usernames else None
                )
                if peer.usernames is not None and len(peer.usernames) > 1:
                    for uname in peer.usernames:
                        usernames.append((peer.id, uname.username.lower()))
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
                    else peer.usernames[0].username.lower() if peer.usernames else None
                )
                if peer.usernames is not None and len(peer.usernames) > 1:
                    for uname in peer.usernames:
                        usernames.append((peer.id, uname.username.lower()))
                peer_type = "channel" if peer.broadcast else "supergroup"
            elif isinstance(peer, raw.types.ChannelForbidden):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                peer_type = "channel" if peer.broadcast else "supergroup"
            else:
                continue

            parsed_peers.append(
                (peer_id, access_hash, peer_type, username, phone_number)
            )

        await self.storage.update_peers(parsed_peers)
        await self.storage.update_usernames(usernames)

        return is_min

    async def handle_updates(self, updates):
        self.last_update_time = datetime.now()

        if isinstance(updates, (raw.types.Updates, raw.types.UpdatesCombined)):
            is_min = any(
                (
                    await self.fetch_peers(updates.users),
                    await self.fetch_peers(updates.chats),
                )
            )

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
                        )
                    )

                if isinstance(update, raw.types.UpdateChannelTooLong):
                    log.info(update)

                if isinstance(update, raw.types.UpdateNewChannelMessage) and is_min:
                    message = update.message

                    if not isinstance(message, raw.types.MessageEmpty):
                        try:
                            diff = await self.invoke(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.resolve_peer(
                                        utils.get_channel_id(channel_id)
                                    ),
                                    filter=raw.types.ChannelMessagesFilter(
                                        ranges=[
                                            raw.types.MessageRange(
                                                min_id=update.message.id,
                                                max_id=update.message.id,
                                            )
                                        ]
                                    ),
                                    pts=pts - pts_count,
                                    limit=pts,
                                )
                            )
                        except ChannelPrivate:
                            pass
                        else:
                            if not isinstance(
                                diff, raw.types.updates.ChannelDifferenceEmpty
                            ):
                                if diff:
                                    users.update({u.id: u for u in diff.users})
                                    chats.update({c.id: c for c in diff.chats})

                self.dispatcher.updates_queue.put_nowait((update, users, chats))
        elif isinstance(
            updates, (raw.types.UpdateShortMessage, raw.types.UpdateShortChatMessage)
        ):
            if not self.skip_updates:
                await self.storage.update_state(
                    (0, updates.pts, None, updates.date, None)
                )

            diff = await self.invoke(
                raw.functions.updates.GetDifference(
                    pts=updates.pts - updates.pts_count, date=updates.date, qts=-1
                )
            )

            if diff.new_messages:
                self.dispatcher.updates_queue.put_nowait(
                    (
                        raw.types.UpdateNewMessage(
                            message=diff.new_messages[0],
                            pts=updates.pts,
                            pts_count=updates.pts_count,
                        ),
                        {u.id: u for u in diff.users},
                        {c.id: c for c in diff.chats},
                    )
                )
            else:
                if diff.other_updates:  # The other_updates list can be empty
                    self.dispatcher.updates_queue.put_nowait(
                        (diff.other_updates[0], {}, {})
                    )
        elif isinstance(updates, raw.types.UpdateShort):
            self.dispatcher.updates_queue.put_nowait((updates.update, {}, {}))
        elif isinstance(updates, raw.types.UpdatesTooLong):
            log.info(updates)

    async def load_session(self):
        await self.storage.open()

        session_empty = any(
            [
                await self.storage.test_mode() is None,
                await self.storage.auth_key() is None,
                await self.storage.user_id() is None,
                await self.storage.is_bot() is None,
            ]
        )

        if session_empty:
            if not self.api_id or not self.api_hash:
                raise AttributeError(
                    "The API key is required for new authorizations. "
                    "More info: https://dawn.github.io/nekozee-docs/start/auth"
                )

            await self.storage.api_id(self.api_id)

            await self.storage.dc_id(2)
            await self.storage.date(0)

            await self.storage.test_mode(self.test_mode)
            await self.storage.auth_key(
                await Auth(
                    self, await self.storage.dc_id(), await self.storage.test_mode()
                ).create()
            )
            await self.storage.user_id(None)
            await self.storage.is_bot(None)
        else:
            if not await self.storage.api_id():
                if self.api_id:
                    await self.storage.api_id(self.api_id)
                else:
                    while True:
                        try:
                            value = int(
                                await ainput("Enter the api_id part of the API key: ")
                            )

                            if value <= 0:
                                print("Invalid value")
                                continue

                            confirm = (
                                await ainput(f'Is "{value}" correct? (y/N): ')
                            ).lower()

                            if confirm == "y":
                                await self.storage.api_id(value)
                                break
                        except Exception as e:
                            print(e)

    def load_plugins(self):
        if self.plugins:
            plugins = self.plugins.copy()

            for option in ["include", "exclude"]:
                if plugins.get(option, []):
                    plugins[option] = [
                        (i.split()[0], i.split()[1:] or None)
                        for i in self.plugins[option]
                    ]
        else:
            return

        if plugins.get("enabled", True):
            root = plugins["root"]
            include = plugins.get("include", [])
            exclude = plugins.get("exclude", [])

            count = 0

            if not include:
                for path in sorted(Path(root.replace(".", "/")).rglob("*.py")):
                    module_path = ".".join(path.parent.parts + (path.stem,))
                    module = import_module(module_path)

                    for name in vars(module).keys():
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(
                                    group, int
                                ):
                                    self.add_handler(handler, group)

                                    log.info(
                                        '[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                            self.name,
                                            type(handler).__name__,
                                            name,
                                            group,
                                            module_path,
                                        )
                                    )

                                    count += 1
                        except Exception:
                            pass
            else:
                for path, handlers in include:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning(
                            '[%s] [LOAD] Ignoring non-existent module "%s"',
                            self.name,
                            module_path,
                        )
                        continue

                    if "__path__" in dir(module):
                        log.warning(
                            '[%s] [LOAD] Ignoring namespace "%s"',
                            self.name,
                            module_path,
                        )
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(
                                    group, int
                                ):
                                    self.add_handler(handler, group)

                                    log.info(
                                        '[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                            self.name,
                                            type(handler).__name__,
                                            name,
                                            group,
                                            module_path,
                                        )
                                    )

                                    count += 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning(
                                    '[{}] [LOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                        self.name, name, module_path
                                    )
                                )

            if exclude:
                for path, handlers in exclude:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning(
                            '[%s] [UNLOAD] Ignoring non-existent module "%s"',
                            self.name,
                            module_path,
                        )
                        continue

                    if "__path__" in dir(module):
                        log.warning(
                            '[%s] [UNLOAD] Ignoring namespace "%s"',
                            self.name,
                            module_path,
                        )
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(
                                    group, int
                                ):
                                    self.remove_handler(handler, group)

                                    log.info(
                                        '[{}] [UNLOAD] {}("{}") from group {} in "{}"'.format(
                                            self.name,
                                            type(handler).__name__,
                                            name,
                                            group,
                                            module_path,
                                        )
                                    )

                                    count -= 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning(
                                    '[{}] [UNLOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                        self.name, name, module_path
                                    )
                                )

            if count > 0:
                log.info(
                    '[{}] Successfully loaded {} plugin{} from "{}"'.format(
                        self.name, count, "s" if count > 1 else "", root
                    )
                )
            else:
                log.warning('[%s] No plugin loaded from "%s"', self.name, root)

    async def handle_download(self, packet):
        (
            file_id,
            directory,
            file_name,
            in_memory,
            file_size,
            progress,
            progress_args,
        ) = packet

        makedirs(directory, exist_ok=True) if not in_memory else None
        temp_file_path = (
            path.abspath(sub("\\\\", "/", path.join(directory, file_name)))
            + ".temp"
        )
        file = BytesIO() if in_memory else open(temp_file_path, "wb")

        try:
            async for chunk in self.get_file(
                file_id,
                file_size,
                0,
                0,
                progress,
                progress_args
            ):
                file.write(chunk)
        except BaseException as e:
            if not in_memory:
                file.close()
                remove(temp_file_path)

            if isinstance(e, CancelledError):
                raise e

            if isinstance(e, (FloodWait, FloodPremiumWait)):
                raise e

            return None
        else:
            if in_memory:
                file.name = file_name
                return file
            else:
                file.close()
                file_path = path.splitext(temp_file_path)[0]
                move(temp_file_path, file_path)
                return file_path

    async def get_file(
        self,
        file_id: FileId,
        file_size: int = 0,
        limit: int = 0,
        offset: int = 0,
        progress: Callable = None,
        progress_args: tuple = (),
    ) -> Optional[AsyncGenerator[bytes, None]]:
        async with self.get_file_semaphore:
            file_type = file_id.file_type

            if file_type == FileType.CHAT_PHOTO:
                if file_id.chat_id > 0:
                    peer = raw.types.InputPeerUser(
                        user_id=file_id.chat_id, access_hash=file_id.chat_access_hash
                    )
                else:
                    if file_id.chat_access_hash == 0:
                        peer = raw.types.InputPeerChat(chat_id=-file_id.chat_id)
                    else:
                        peer = raw.types.InputPeerChannel(
                            channel_id=utils.get_channel_id(file_id.chat_id),
                            access_hash=file_id.chat_access_hash,
                        )

                location = raw.types.InputPeerPhotoFileLocation(
                    peer=peer,
                    photo_id=file_id.media_id,
                    big=file_id.thumbnail_source == ThumbnailSource.CHAT_PHOTO_BIG,
                )
            elif file_type == FileType.PHOTO:
                location = raw.types.InputPhotoFileLocation(
                    id=file_id.media_id,
                    access_hash=file_id.access_hash,
                    file_reference=file_id.file_reference,
                    thumb_size=file_id.thumbnail_size,
                )
            else:
                location = raw.types.InputDocumentFileLocation(
                    id=file_id.media_id,
                    access_hash=file_id.access_hash,
                    file_reference=file_id.file_reference,
                    thumb_size=file_id.thumbnail_size,
                )

            current = 0
            total = abs(limit) or (1 << 31) - 1
            chunk_size = 1024 * 1024
            offset_bytes = abs(offset) * chunk_size

            dc_id = file_id.dc_id

            session = Session(
                self,
                dc_id,
                (
                    await Auth(self, dc_id, await self.storage.test_mode()).create()
                    if dc_id != await self.storage.dc_id()
                    else await self.storage.auth_key()
                ),
                await self.storage.test_mode(),
                is_media=True,
            )

            try:
                await session.start()

                if dc_id != await self.storage.dc_id():
                    exported_auth = await self.invoke(
                        raw.functions.auth.ExportAuthorization(dc_id=dc_id)
                    )

                    await session.invoke(
                        raw.functions.auth.ImportAuthorization(
                            id=exported_auth.id, bytes=exported_auth.bytes
                        )
                    )

                r = await session.invoke(
                    raw.functions.upload.GetFile(
                        location=location, offset=offset_bytes, limit=chunk_size
                    ),
                    sleep_threshold=30,
                )

                if isinstance(r, raw.types.upload.File):
                    while True:
                        chunk = r.bytes

                        yield chunk

                        current += 1
                        offset_bytes += chunk_size

                        if progress:
                            func = partial(
                                progress,
                                (
                                    min(offset_bytes, file_size)
                                    if file_size != 0
                                    else offset_bytes
                                ),
                                file_size,
                                *progress_args,
                            )

                            if iscoroutinefunction(progress):
                                await func()
                            else:
                                await self.loop.run_in_executor(self.executor, func)

                        if len(chunk) < chunk_size or current >= total:
                            break

                        r = await session.invoke(
                            raw.functions.upload.GetFile(
                                location=location, offset=offset_bytes, limit=chunk_size
                            ),
                            sleep_threshold=30,
                        )

                elif isinstance(r, raw.types.upload.FileCdnRedirect):
                    cdn_session = Session(
                        self,
                        r.dc_id,
                        await Auth(
                            self, r.dc_id, await self.storage.test_mode()
                        ).create(),
                        await self.storage.test_mode(),
                        is_media=True,
                        is_cdn=True,
                    )

                    try:
                        await cdn_session.start()

                        while True:
                            r2 = await cdn_session.invoke(
                                raw.functions.upload.GetCdnFile(
                                    file_token=r.file_token,
                                    offset=offset_bytes,
                                    limit=chunk_size,
                                )
                            )

                            if isinstance(r2, raw.types.upload.CdnFileReuploadNeeded):
                                try:
                                    await session.invoke(
                                        raw.functions.upload.ReuploadCdnFile(
                                            file_token=r.file_token,
                                            request_token=r2.request_token,
                                        )
                                    )
                                except VolumeLocNotFound:
                                    break
                                else:
                                    continue

                            chunk = r2.bytes

                            decrypted_chunk = aes.ctr256_decrypt(
                                chunk,
                                r.encryption_key,
                                bytearray(
                                    r.encryption_iv[:-4]
                                    + (offset_bytes // 16).to_bytes(4, "big")
                                ),
                            )

                            hashes = await session.invoke(
                                raw.functions.upload.GetCdnFileHashes(
                                    file_token=r.file_token, offset=offset_bytes
                                )
                            )

                            for i, h in enumerate(hashes):
                                cdn_chunk = decrypted_chunk[
                                    h.limit * i : h.limit * (i + 1)
                                ]
                                CDNFileHashMismatch.check(
                                    h.hash == sha256(cdn_chunk).digest(),
                                    "h.hash == sha256(cdn_chunk).digest()",
                                )

                            yield decrypted_chunk

                            current += 1
                            offset_bytes += chunk_size

                            if progress:
                                func = partial(
                                    progress,
                                    (
                                        min(offset_bytes, file_size)
                                        if file_size != 0
                                        else offset_bytes
                                    ),
                                    file_size,
                                    *progress_args,
                                )

                                if iscoroutinefunction(progress):
                                    await func()
                                else:
                                    await self.loop.run_in_executor(self.executor, func)

                            if len(chunk) < chunk_size or current >= total:
                                break
                    except Exception as e:
                        raise e
                    finally:
                        await cdn_session.stop()
            except pyrogram.StopTransmission:
                raise
            except (FloodWait, FloodPremiumWait):
                raise
            except Exception as e:
                log.exception(e)
            finally:
                await session.stop()

    @lru_cache(maxsize=128)
    def guess_mime_type(self, filename: str) -> Optional[str]:
        return self.mimetypes.guess_type(filename)[0]

    @lru_cache(maxsize=128)
    def guess_extension(self, mime_type: str) -> Optional[str]:
        return self.mimetypes.guess_extension(mime_type)

class Cache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.store = OrderedDict()

    def __getitem__(self, key):
        value = self.store.pop(key, None)
        if value is not None:
            # Reinsert the accessed item as the most recent one
            self.store[key] = value
        return value

    def __setitem__(self, key, value):
        if key in self.store:
            del self.store[key]

        self.store[key] = value

        if len(self.store) > self.capacity:
            self.store.popitem(last=False)  # Remove the oldest item