# ruff: noqa: RUF006
from __future__ import annotations

import asyncio
import contextlib
import logging
import os
from hashlib import sha1
from io import BytesIO

import pyrogram
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import mtproto
from pyrogram.errors import (
    AuthKeyDuplicated,
    BadMsgNotification,
    FloodWait,
    InternalServerError,
    RPCError,
    SecurityCheckMismatch,
    ServiceUnavailable,
)
from pyrogram.raw.all import layer
from pyrogram.raw.core import FutureSalts, Int, MsgContainer, TLObject

from .internals import MsgFactory, MsgId

log = logging.getLogger(__name__)


class Result:
    def __init__(self) -> None:
        self.value = None
        self.event = asyncio.Event()


class Session:
    START_TIMEOUT = 1
    WAIT_TIMEOUT = 15
    SLEEP_THRESHOLD = 10
    MAX_RETRIES = 5
    ACKS_THRESHOLD = 8
    PING_INTERVAL = 5

    def __init__(
        self,
        client: pyrogram.Client,
        dc_id: int,
        auth_key: bytes,
        test_mode: bool,
        is_media: bool = False,
        is_cdn: bool = False,
    ) -> None:
        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.test_mode = test_mode
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.connection = None

        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.session_id = os.urandom(8)
        self.msg_factory = MsgFactory()

        self.salt = 0

        self.pending_acks = set()

        self.results = {}

        self.stored_msg_ids = []

        self.ping_task = None
        self.ping_task_event = asyncio.Event()

        self.network_task = None

        self.is_connected = asyncio.Event()

        self.loop = asyncio.get_event_loop()

    async def start(self):
        while True:
            self.connection = Connection(
                self.dc_id,
                self.test_mode,
                self.client.ipv6,
                self.client.proxy,
                self.is_media,
            )

            try:
                await self.connection.connect()

                self.network_task = self.loop.create_task(self.network_worker())

                await self.send(
                    raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT
                )

                if not self.is_cdn:
                    await self.send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=await self.client.storage.api_id(),
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",
                                query=raw.functions.help.GetConfig(),
                            ),
                        ),
                        timeout=self.START_TIMEOUT,
                    )

                self.ping_task = self.loop.create_task(self.ping_worker())

                log.info("Session initialized: Layer %s", layer)
                log.info(
                    "Device: %s - %s",
                    self.client.device_model,
                    self.client.app_version,
                )
                log.info(
                    "System: %s (%s)",
                    self.client.system_version,
                    self.client.lang_code,
                )

            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, TimeoutError, RPCError):
                await self.stop()
            except Exception as e:
                await self.stop()
                raise e
            else:
                break

        self.is_connected.set()

        log.info("Session started")

    async def stop(self):
        self.is_connected.clear()

        self.ping_task_event.set()

        if self.ping_task is not None:
            await self.ping_task

        self.ping_task_event.clear()

        await self.connection.close()

        if self.network_task:
            await self.network_task

        for i in self.results.values():
            i.event.set()

        if not self.is_media and callable(self.client.disconnect_handler):
            try:
                await self.client.disconnect_handler(self.client)
            except Exception as e:
                log.error(e, exc_info=True)

        log.info("Session stopped")

    async def restart(self):
        await self.stop()
        await self.start()

    async def handle_packet(self, packet):
        try:
            data = await self.loop.run_in_executor(
                pyrogram.crypto_executor,
                mtproto.unpack,
                BytesIO(packet),
                self.session_id,
                self.auth_key,
                self.auth_key_id,
                self.stored_msg_ids,
            )
        except SecurityCheckMismatch:
            return

        messages = (
            data.body.messages if isinstance(data.body, MsgContainer) else [data]
        )

        log.debug("Received:")
        log.debug(data)

        for msg in messages:
            if msg.seq_no == 0:
                MsgId.set_server_time(msg.msg_id / (2**32))

            if msg.seq_no % 2 != 0:
                if msg.msg_id in self.pending_acks:
                    continue
                self.pending_acks.add(msg.msg_id)

            if isinstance(
                msg.body, raw.types.MsgDetailedInfo | raw.types.MsgNewDetailedInfo
            ):
                self.pending_acks.add(msg.body.answer_msg_id)
                continue

            if isinstance(msg.body, raw.types.NewSessionCreated):
                continue

            msg_id = None

            if isinstance(
                msg.body, raw.types.BadMsgNotification | raw.types.BadServerSalt
            ):
                msg_id = msg.body.bad_msg_id
            elif isinstance(msg.body, FutureSalts | raw.types.RpcResult):
                msg_id = msg.body.req_msg_id
            elif isinstance(msg.body, raw.types.Pong):
                msg_id = msg.body.msg_id
            elif self.client is not None:
                self.loop.create_task(self.client.handle_updates(msg.body))

            if msg_id in self.results:
                self.results[msg_id].value = getattr(msg.body, "result", msg.body)
                self.results[msg_id].event.set()

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.debug("Sending %s acks", len(self.pending_acks))

            try:
                await self.send(
                    raw.types.MsgsAck(msg_ids=list(self.pending_acks)), False
                )
            except (OSError, TimeoutError):
                pass
            else:
                self.pending_acks.clear()

    async def ping_worker(self):
        log.info("PingTask started")

        while True:
            try:
                await asyncio.wait_for(
                    self.ping_task_event.wait(), self.PING_INTERVAL
                )
            except asyncio.TimeoutError:
                pass
            else:
                break

            with contextlib.suppress(OSError, TimeoutError, RPCError):
                await self.send(
                    raw.functions.PingDelayDisconnect(
                        ping_id=0, disconnect_delay=self.WAIT_TIMEOUT + 10
                    ),
                    False,
                )

        log.info("PingTask stopped")

    async def network_worker(self):
        log.info("NetworkTask started")

        while True:
            packet = await self.connection.recv()

            if packet is None or len(packet) == 4:
                if packet:
                    log.warning(f'Server sent "{Int.read(BytesIO(packet))}"')

                if self.is_connected.is_set():
                    self.loop.create_task(self.restart())

                break

            self.loop.create_task(self.handle_packet(packet))

        log.info("NetworkTask stopped")

    async def send(
        self,
        data: TLObject,
        wait_response: bool = True,
        timeout: float = WAIT_TIMEOUT,
        retry: int = 0,
    ):
        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        log.debug("Sent:")
        log.debug(message)

        payload = await self.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.pack,
            message,
            self.salt,
            self.session_id,
            self.auth_key,
            self.auth_key_id,
        )

        try:
            await self.connection.send(payload)
        except OSError as e:
            self.results.pop(msg_id, None)
            raise e

        if wait_response:
            try:
                await asyncio.wait_for(self.results[msg_id].event.wait(), timeout)
            except asyncio.TimeoutError:
                pass
            finally:
                result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError
            if isinstance(result, raw.types.RpcError):
                if isinstance(
                    data,
                    raw.functions.InvokeWithoutUpdates
                    | raw.functions.InvokeWithTakeout,
                ):
                    data = data.query

                RPCError.raise_it(result, type(data))
                return None
            if isinstance(result, raw.types.BadMsgNotification):
                if retry > 1:
                    raise BadMsgNotification(result.error_code)
                self._handle_bad_notification()
                await self.send(data, wait_response, timeout, retry + 1)
                return None
            if isinstance(result, raw.types.BadServerSalt):
                self.salt = result.new_server_salt
                return await self.send(data, wait_response, timeout)
            return result
        return None

    def _handle_bad_notification(self) -> None:
        new_msg_id = MsgId()
        if self.stored_msg_ids[len(self.stored_msg_ids) - 1] >= new_msg_id:
            new_msg_id = self.stored_msg_ids[len(self.stored_msg_ids) - 1] + 4
            log.debug(
                "Changing msg_id old=%s new=%s",
                self.stored_msg_ids[len(self.stored_msg_ids) - 1],
                new_msg_id,
            )
        self.stored_msg_ids[len(self.stored_msg_ids) - 1] = new_msg_id

    async def invoke(
        self,
        query: TLObject,
        retries: int = MAX_RETRIES,
        timeout: float = WAIT_TIMEOUT,
        sleep_threshold: float = SLEEP_THRESHOLD,
    ):
        with contextlib.suppress(asyncio.TimeoutError):
            await asyncio.wait_for(self.is_connected.wait(), self.WAIT_TIMEOUT)

        if isinstance(
            query,
            raw.functions.InvokeWithoutUpdates | raw.functions.InvokeWithTakeout,
        ):
            inner_query = query.query
        else:
            inner_query = query

        query_name = ".".join(inner_query.QUALNAME.split(".")[1:])

        while True:
            try:
                return await self.send(query, timeout=timeout)
            except FloodWait as e:
                amount = e.value

                if amount > sleep_threshold >= 0:
                    raise

                log.warning(
                    '[%s] Waiting for %s seconds before continuing (required by "%s")',
                    self.client.name,
                    amount,
                    query_name,
                )

                await asyncio.sleep(amount)
            except (
                OSError,
                TimeoutError,
                InternalServerError,
                ServiceUnavailable,
            ) as e:
                if retries == 0:
                    raise e from None

                (log.warning if retries < 2 else log.info)(
                    f'[{Session.MAX_RETRIES - retries + 1}] Retrying "{query_name}" due to {str(e) or repr(e)}'
                )

                await asyncio.sleep(0.5)

                return await self.invoke(query, retries - 1, timeout)
