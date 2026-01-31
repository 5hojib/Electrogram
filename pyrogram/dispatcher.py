# ruff: noqa: ARG001
from __future__ import annotations

import asyncio
import inspect
import logging
from collections import OrderedDict

import pyrogram
from pyrogram import errors, raw, utils
from pyrogram.handlers import (
    DisconnectHandler,
    RawUpdateHandler,
)
from pyrogram.raw.types import (
    UpdateNewChannelMessage,
    UpdateNewMessage,
    UpdateNewScheduledMessage,
)

log = logging.getLogger(__name__)


class Dispatcher:
    def __init__(self, client: pyrogram.Client) -> None:
        self.client = client
        self.loop = asyncio.get_event_loop()
        self.handler_worker_tasks = []
        self.locks_list = []
        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

    async def start(self) -> None:
        if not self.client.no_updates:
            for _i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(self.handler_worker(self.locks_list[-1])),
                )

            log.info("Started %s HandlerTasks", self.client.workers)

            if not self.client.skip_updates:
                states = await self.client.storage.update_state()

                if not states:
                    log.info("No states found, skipping recovery.")
                    return

                message_updates_counter = 0
                other_updates_counter = 0

                for state in states:
                    id, local_pts, _, local_date, _ = state

                    prev_pts = 0

                    while True:
                        try:
                            diff = await self.client.invoke(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.client.resolve_peer(id),
                                    filter=raw.types.ChannelMessagesFilterEmpty(),
                                    pts=local_pts,
                                    limit=10000,
                                )
                                if id < 0
                                else raw.functions.updates.GetDifference(
                                    pts=local_pts,
                                    date=local_date,
                                    qts=0,
                                ),
                            )
                        except (
                            errors.ChannelPrivate,
                            errors.ChannelInvalid,
                        ):
                            break

                        if isinstance(
                            diff,
                            (
                                raw.types.updates.DifferenceEmpty,
                                raw.types.updates.DifferenceTooLong,
                            ),
                        ):
                            break
                        if isinstance(diff, raw.types.updates.Difference):
                            local_pts = diff.state.pts
                        elif isinstance(diff, raw.types.updates.DifferenceSlice):
                            local_pts = diff.intermediate_state.pts
                            local_date = diff.intermediate_state.date

                            if prev_pts == local_pts:
                                break

                            prev_pts = local_pts
                        elif isinstance(
                            diff,
                            (
                                raw.types.updates.ChannelDifferenceEmpty,
                                raw.types.updates.ChannelDifferenceTooLong,
                            ),
                        ):
                            break
                        if isinstance(diff, raw.types.updates.ChannelDifference):
                            local_pts = diff.pts

                        users = {i.id: i for i in diff.users}
                        chats = {i.id: i for i in diff.chats}

                        for message in diff.new_messages:
                            message_updates_counter += 1
                            self.updates_queue.put_nowait(
                                (
                                    raw.types.UpdateNewMessage(
                                        message=message,
                                        pts=local_pts,
                                        pts_count=-1,
                                    )
                                    if id == self.client.me.id
                                    else raw.types.UpdateNewChannelMessage(
                                        message=message,
                                        pts=local_pts,
                                        pts_count=-1,
                                    ),
                                    users,
                                    chats,
                                ),
                            )

                        for update in diff.other_updates:
                            other_updates_counter += 1
                            self.updates_queue.put_nowait((update, users, chats))

                        if isinstance(
                            diff,
                            (
                                raw.types.updates.Difference,
                                raw.types.updates.ChannelDifference,
                            ),
                        ):
                            break

                    await self.client.storage.update_state(id)

                log.info(
                    "Recovered %s messages and %s updates.",
                    message_updates_counter,
                    other_updates_counter,
                )

    async def stop(self) -> None:
        if not self.client.no_updates:
            for _i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()

            log.info("Stopped %s HandlerTasks", self.client.workers)

    def add_handler(self, handler, group: int) -> None:
        async def fn() -> None:
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    self.groups[group] = []
                    self.groups = OrderedDict(sorted(self.groups.items()))

                self.groups[group].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    def remove_handler(self, handler, group: int) -> None:
        async def fn() -> None:
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    raise ValueError(
                        f"Group {group} does not exist. Handler was not removed.",
                    )

                self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    async def handler_worker(self, lock) -> None:
        while True:
            packet = await self.updates_queue.get()

            if packet is None:
                break

            try:
                update, users, chats = packet

                async with lock:
                    for group in self.groups.values():
                        for handler in group:
                            args = None

                            if isinstance(handler, RawUpdateHandler):
                                args = (update, users, chats)

                            if args is None:
                                continue

                            try:
                                if inspect.iscoroutinefunction(handler.callback):
                                    await handler.callback(self.client, *args)
                                else:
                                    await self.loop.run_in_executor(
                                        self.client.executor,
                                        handler.callback,
                                        self.client,
                                        *args,
                                    )
                            except pyrogram.StopPropagationError:
                                raise
                            except pyrogram.ContinuePropagationError:
                                continue
                            except Exception as e:
                                log.exception(e)

                            break
            except pyrogram.StopPropagationError:
                pass
            except Exception as e:
                log.exception(e)
            finally:
                self.updates_queue.task_done()
