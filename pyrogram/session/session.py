from asyncio import get_event_loop, Event, create_task, TimeoutError, sleep, wait_for
from bisect import insort
from logging import getLogger
from os import urandom
from time import time
from hashlib import sha1
from io import BytesIO

from pyrogram.raw.all import layer

import pyrogram
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import mtproto
from pyrogram.errors import (
    RPCError,
    InternalServerError,
    AuthKeyDuplicated,
    FloodWait,
    FloodPremiumWait,
    ServiceUnavailable,
    BadMsgNotification,
    SecurityCheckMismatch,
    Unauthorized,
)
from pyrogram.raw.core import TLObject, MsgContainer, FutureSalts
from .internals import MsgId, MsgFactory

log = getLogger(__name__)


class Result:
    def __init__(self):
        self.value = None
        self.event = Event()

class Session:
    START_TIMEOUT = 5
    WAIT_TIMEOUT = 15
    RECONN_TIMEOUT = 5
    SLEEP_THRESHOLD = 10
    MAX_RETRIES = 20
    ACKS_THRESHOLD = 10
    PING_INTERVAL = 5
    STORED_MSG_IDS_MAX_SIZE = 1000 * 2
    RECONNECT_THRESHOLD = 13
    RE_START_RANGE = range(4)

    TRANSPORT_ERRORS = {
        404: "auth key not found",
        429: "transport flood",
        444: "invalid DC",
    }

    def __init__(
        self,
        client: "pyrogram.Client",
        dc_id: int,
        auth_key: bytes,
        test_mode: bool,
        is_media: bool = False,
        is_cdn: bool = False,
    ):
        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.test_mode = test_mode
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.auth_key_id = sha1(auth_key).digest()[-8:]
        self.session_id = urandom(8)
        self.msg_factory = MsgFactory()
        self.salt = 0

        self.pending_acks = set()
        self.results = {}
        self.stored_msg_ids = []
        self.ping_task = None
        self.ping_task_event = Event()
        self.recv_task = None
        self.is_started = Event()

        self.loop = get_event_loop()
        self.instant_stop = False
        self.last_reconnect_attempt = None
        self.currently_restarting = False
        self.currently_stopping = False

    async def start(self):
        while True:
            if self.instant_stop:
                log.info("Session init force stopped (loop)")
                return  # stop instantly

            self.connection = self.client.connection_factory(
                dc_id=self.dc_id,
                test_mode=self.test_mode,
                ipv6=self.client.ipv6,
                proxy=self.client.proxy,
                alt_port=self.client.alt_port,
                media=self.is_media,
                protocol_factory=self.client.protocol_factory,
            )

            try:
                await self.connection.connect()
                self.recv_task = create_task(self.recv_worker())

                await self.send(
                    raw.functions.Ping(ping_id=0), timeout=self.START_TIMEOUT
                )

                if not self.is_cdn:
                    await self.send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=await self.client.storage.api_id(), # type: ignore
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.system_lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack=self.client.lang_pack,
                                query=raw.functions.help.GetConfig(),
                                params=self.client.init_params, # type: ignore
                            ),
                        ),
                        timeout=self.START_TIMEOUT,
                    )

                self.ping_task = create_task(self.ping_worker())

                log.info("Session initialized: Layer %s", layer)
                log.info(
                    "Device: %s - %s", self.client.device_model, self.client.app_version
                )
                log.info(
                    "System: %s (%s)", self.client.system_version, self.client.lang_code
                )
            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, RPCError):
                await self.stop()
            except Exception as e:
                await self.stop()
                raise e
            else:
                break

        self.is_started.set()
        log.info("Session started")

    async def stop(self, restart: bool = False):
        if self.currently_stopping:
            return  # don't stop twice
        if self.instant_stop:
            log.info("Session stop process stopped")
            return  # stop doing anything instantly, client is manually handling

        try:
            self.currently_stopping = True
            self.is_started.clear()
            self.stored_msg_ids.clear()

            if restart:
                self.instant_stop = True  # tell all funcs that we want to stop

            self.ping_task_event.set()
            if self.ping_task:
                try:
                    await wait_for(self.ping_task, timeout=self.RECONN_TIMEOUT)
                except TimeoutError:
                    self.ping_task.cancel()
            self.ping_task_event.clear()

            if self.connection:
                try:
                    await wait_for(
                        self.connection.close(), timeout=self.RECONN_TIMEOUT
                    )
                except Exception:
                    pass

            if self.recv_task:
                try:
                    await wait_for(self.recv_task, timeout=self.RECONN_TIMEOUT)
                except TimeoutError:
                    self.recv_task.cancel()

            if not self.is_media and callable(self.client.disconnect_handler):
                try:
                    await self.client.disconnect_handler(self.client) # type: ignore
                except Exception as e:
                    log.exception(e)

            log.info("Session stopped")
        finally:
            self.currently_stopping = False
            if restart:
                self.instant_stop = False  # reset

    async def restart(self):
        if self.currently_restarting:
            return  # don't restart twice
        if self.instant_stop:
            return  # stop instantly

        try:
            self.currently_restarting = True
            now = time()
            if (
                self.last_reconnect_attempt
                and (now - self.last_reconnect_attempt) < self.RECONNECT_THRESHOLD
            ):
                to_wait = self.RECONNECT_THRESHOLD + int(
                    self.RECONNECT_THRESHOLD - (now - self.last_reconnect_attempt)
                )
                log.warning(
                    f"[nekozee] Client [{self.client.name}] is reconnecting too frequently, sleeping for {to_wait} seconds"
                )
                await sleep(to_wait)

            self.last_reconnect_attempt = time()
            await self.stop(restart=True)
            for try_ in self.RE_START_RANGE:  # sometimes, the DB says "no" 😬
                try:
                    await self.start()
                    break
                except ValueError as e:  # SQLite error
                    try:
                        await self.client.load_session()
                        log.info(
                            f"[nekozee] Client [{self.client.name}] re-starting got SQLite error, connected to DB successfully. try %s; exc: %s %s",
                            try_,
                            type(e).__name__,
                            e,
                        )
                    except Exception as e:
                        log.warning(
                            f"[nekozee] Client [{self.client.name}] failed re-starting SQLite DB, try %s; exc: %s %s",
                            try_,
                            type(e).__name__,
                            e,
                        )
                except Exception as e:
                    log.warning(
                        f"[nekozee] Client [{self.client.name}] failed re-starting, try %s; exc: %s %s",
                        try_,
                        type(e).__name__,
                        e,
                    )
        finally:
            self.currently_restarting = False

    async def handle_packet(self, packet):
        if self.instant_stop:
            log.info("Stopped packet handler")
            return  # stop instantly

        data = await self.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.unpack,
            BytesIO(packet),
            self.session_id,
            self.auth_key,
            self.auth_key_id,
        )

        messages = data.body.messages if isinstance(data.body, MsgContainer) else [data]

        log.debug("Received: %s", data)

        for msg in messages:
            if msg.seq_no % 2 != 0:
                if msg.msg_id in self.pending_acks:
                    continue
                else:
                    self.pending_acks.add(msg.msg_id)

            if len(self.stored_msg_ids) > Session.STORED_MSG_IDS_MAX_SIZE:
                del self.stored_msg_ids[: Session.STORED_MSG_IDS_MAX_SIZE // 2]

            try:
                if self.stored_msg_ids and msg.msg_id < self.stored_msg_ids[0]:
                    raise SecurityCheckMismatch(
                        "The msg_id is lower than all the stored values"
                    )

                if msg.msg_id in self.stored_msg_ids:
                    raise SecurityCheckMismatch(
                        "The msg_id is equal to any of the stored values"
                    )

                time_diff = (msg.msg_id - MsgId()) / 2**32

                if time_diff > 30:
                    raise SecurityCheckMismatch(
                        "The msg_id belongs to over 30 seconds in the future. "
                        "Most likely the client time has to be synchronized."
                    )

                if time_diff < -300:
                    raise SecurityCheckMismatch(
                        "The msg_id belongs to over 300 seconds in the past. "
                        "Most likely the client time has to be synchronized."
                    )
            except SecurityCheckMismatch as e:
                log.info("Discarding packet: %s", e)
                await self.connection.close()
                return
            else:
                insort(self.stored_msg_ids, msg.msg_id)

            if isinstance(msg.body, (
                raw.types.MsgDetailedInfo,
                raw.types.MsgNewDetailedInfo
            )):
                self.pending_acks.add(msg.body.answer_msg_id)
                continue

            if isinstance(
                msg.body,
                raw.types.NewSessionCreated
            ):
                continue

            msg_id = None

            if isinstance(msg.body, (
                raw.types.BadMsgNotification,
                raw.types.BadServerSalt
            )):
                msg_id = msg.body.bad_msg_id
            elif isinstance(msg.body, (
                FutureSalts,
                raw.types.RpcResult
            )):
                msg_id = msg.body.req_msg_id
            elif isinstance(
                msg.body,
                raw.types.Pong
            ):
                msg_id = msg.body.msg_id
            else:
                if self.client:
                    self.loop.create_task(self.client.handle_updates(msg.body))

            if msg_id and msg_id in self.results:
                self.results[msg_id].value = getattr(
                    msg.body,
                    "result",
                    msg.body
                )
                self.results[msg_id].event.set()

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.debug("Sending %s acks", len(self.pending_acks))

            try:
                await self.send(
                    raw.types.MsgsAck(msg_ids=list(self.pending_acks)),
                    False
                )
            except OSError:
                pass
            else:
                self.pending_acks.clear()

    async def ping_worker(self):
        log.info("PingTask started")

        while True:
            if self.instant_stop:
                log.info("PingTask force stopped (loop)")
                return  # stop instantly

            try:
                await wait_for(self.ping_task_event.wait(), self.PING_INTERVAL)
            except TimeoutError:
                pass
            else:
                break

            try:
                await self.send(
                    raw.functions.PingDelayDisconnect(
                        ping_id=0, disconnect_delay=self.WAIT_TIMEOUT + 10
                    ),
                    False,
                )
            except OSError:
                create_task(self.restart())
                break
            except RPCError:
                pass

        log.info("PingTask stopped")

    async def recv_worker(self):
        log.info("NetworkTask started")

        while True:
            if self.instant_stop:
                log.info("NetworkTask force stopped (loop)")
                return  # stop instantly

            packet = await self.connection.recv()

            if packet is None or len(packet) == 4:
                if packet:
                    error_code = -int.from_bytes(packet, byteorder='little')

                    if error_code == 404:
                        raise Unauthorized(
                            "Auth key not found in the system. You must delete your session file "
                            "and log in again with your phone number or bot token."
                        )

                    log.warning(
                        "[%s] Server sent transport error: %s (%s)",
                        self.client.name,
                        error_code,
                        Session.TRANSPORT_ERRORS.get(error_code, "unknown error"),
                    )

                if self.is_started.is_set():
                    create_task(self.restart())

                break

            create_task(self.handle_packet(packet))

        log.info("NetworkTask stopped")

    async def send(
        self,
        data: TLObject,
        wait_response: bool = True,
        timeout: float = WAIT_TIMEOUT,
        retry: int = 0,
    ):
        if self.instant_stop:
            return  # stop instantly

        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        log.debug("Sent: %s", message)

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
                await wait_for(self.results[msg_id].event.wait(), timeout)
            except TimeoutError:
                pass

            result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError("Request timed out")

            if isinstance(result, raw.types.RpcError):
                if isinstance(
                    data,
                    (
                        raw.functions.InvokeWithoutUpdates,
                        raw.functions.InvokeWithTakeout,
                    ),
                ):
                    data = data.query

                RPCError.raise_it(result, type(data))

            if isinstance(result, raw.types.BadMsgNotification):
                if retry > 1:
                    raise BadMsgNotification(result.error_code)

                self._handle_bad_notification()
                await self.send(data, wait_response, timeout, retry + 1)

            if isinstance(result, raw.types.BadServerSalt):
                self.salt = result.new_server_salt
                return await self.send(data, wait_response, timeout)

            return result

    def _handle_bad_notification(self):
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
        if isinstance(
            query, (raw.functions.InvokeWithoutUpdates, raw.functions.InvokeWithTakeout)
        ):
            inner_query = query.query
        else:
            inner_query = query

        query_name = ".".join(inner_query.QUALNAME.split(".")[1:])

        while retries > 0:
            # sleep until the restart is performed
            if self.currently_restarting:
                while self.currently_restarting:
                    await sleep(1)

            if self.instant_stop:
                return  # stop instantly

            if not self.is_started.is_set():
                await self.is_started.wait()

            try:
                return await self.send(query, timeout=timeout)
            except (FloodWait, FloodPremiumWait) as e:
                amount = e.value

                if amount > sleep_threshold >= 0: # type: ignore
                    raise

                log.warning(
                    '[%s] Waiting for %s seconds before continuing (required by "%s")',
                    self.client.name,
                    amount,
                    query_name,
                )

                await sleep(amount) # type: ignore
            except (
                OSError,
                RuntimeError,
                InternalServerError,
                ServiceUnavailable,
                TimeoutError,
            ) as e:
                retries -= 1
                if retries == 0:
                    self.client.updates_invoke_error = e # type: ignore
                    raise

                if (isinstance(e, (OSError, RuntimeError)) and "handler" in str(e)) or (
                    isinstance(e, TimeoutError)
                ):
                    (log.warning if retries < 2 else log.info)(
                        '[%s] [%s] Reconnecting session requesting "%s", due to: %s',
                        self.client.name,
                        Session.MAX_RETRIES - retries,
                        query_name,
                        str(e) or repr(e),
                    )
                    create_task(self.restart())
                else:
                    (log.warning if retries < 2 else log.info)(
                        '[%s] [%s] Retrying "%s" due to: %s',
                        self.client.name,
                        Session.MAX_RETRIES - retries,
                        query_name,
                        str(e) or repr(e),
                    )

                await sleep(1)
            except Exception as e:
                self.client.updates_invoke_error = e # type: ignore
                raise

        raise TimeoutError("Exceeded maximum number of retries")
