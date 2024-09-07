from __future__ import annotations

from asyncio import Queue, gather, sleep
from functools import partial
from hashlib import md5
from inspect import iscoroutinefunction
from io import SEEK_END
from logging import getLogger
from math import ceil
from pathlib import PurePath
from typing import TYPE_CHECKING, BinaryIO

import pyrogram
from pyrogram import StopTransmission, raw
from pyrogram.session import Session

if TYPE_CHECKING:
    from collections.abc import Callable

log = getLogger(__name__)


class SaveFile:
    async def save_file(
        self: pyrogram.Client,
        path: str | BinaryIO,
        file_id: int | None = None,
        file_part: int = 0,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ):
        async with self.save_file_semaphore:
            if path is None:
                return None

            async def worker(session):
                while True:
                    data = await queue.get()
                    if data is None:
                        return
                    for attempt in range(3):
                        try:
                            await session.invoke(data)
                            break
                        except Exception as e:
                            log.warning(f"Retrying part due to error: {e}")
                            await sleep(2**attempt)

            def create_rpc(chunk, file_part, is_big, file_id, file_total_parts):
                if is_big:
                    return raw.functions.upload.SaveBigFilePart(
                        file_id=file_id,
                        file_part=file_part,
                        file_total_parts=file_total_parts,
                        bytes=chunk,
                    )
                else:
                    return raw.functions.upload.SaveFilePart(
                        file_id=file_id, file_part=file_part, bytes=chunk
                    )

            part_size = 512 * 1024
            queue = Queue(16)

            with (
                open(path, "rb", buffering=4096)
                if isinstance(path, str | PurePath)
                else path
            ) as fp:
                file_name = getattr(fp, "name", "file.jpg")
                fp.seek(0, SEEK_END)
                file_size = fp.tell()
                fp.seek(0)

                if file_size == 0:
                    raise ValueError("File size equals to 0 B")

                file_size_limit_mib = (
                    4000
                    if self.me.is_premium  # type: ignore
                    else 2000
                )

                if file_size > file_size_limit_mib * 1024 * 1024:
                    raise ValueError(
                        f"Can't upload files bigger than {file_size_limit_mib} MiB"
                    )

                file_total_parts = ceil(file_size / part_size)
                is_big = file_size > 100 * 1024 * 1024
                pool_size = 2 if is_big else 1
                workers_count = 10 if is_big else 1
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None

                pool = [
                    Session(
                        self,
                        await self.storage.dc_id(),  # type: ignore
                        await self.storage.auth_key(),  # type: ignore
                        await self.storage.test_mode(),  # type: ignore
                        is_media=True,
                    )
                    for _ in range(pool_size)
                ]

                workers = [
                    self.loop.create_task(worker(session))
                    for session in pool
                    for _ in range(workers_count)
                ]

                try:
                    for session in pool:
                        await session.start()

                    fp.seek(part_size * file_part)
                    next_chunk_task = self.loop.create_task(
                        self.preload(fp, part_size)
                    )

                    while True:
                        chunk = await next_chunk_task
                        next_chunk_task = self.loop.create_task(
                            self.preload(fp, part_size)
                        )

                        if not chunk:
                            if not is_big and not is_missing_part:
                                md5_sum = md5_sum.hexdigest()  # type: ignore
                            break

                        await queue.put(
                            create_rpc(
                                chunk, file_part, is_big, file_id, file_total_parts
                            )
                        )

                        if is_missing_part:
                            return None

                        if not is_big and not is_missing_part:
                            md5_sum.update(chunk)  # type: ignore

                        file_part += 1

                        if progress and file_part % (file_total_parts // 10) == 0:
                            func = partial(
                                progress,
                                min(file_part * part_size, file_size),
                                file_size,
                                *progress_args,
                            )

                            if iscoroutinefunction(progress):
                                await func()
                            else:
                                await self.loop.run_in_executor(self.executor, func)
                except StopTransmission:
                    raise
                except Exception as e:
                    log.error(
                        f"Error during file upload at part {file_part}: {e}",
                        exc_info=True,
                    )
                else:
                    if is_big:
                        return raw.types.InputFileBig(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                        )
                    else:
                        return raw.types.InputFile(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                            md5_checksum=md5_sum,  # type: ignore
                        )
                finally:
                    for _ in workers:
                        await queue.put(None)

                    await gather(*workers)

                    for session in pool:
                        await session.stop()

    async def preload(self, fp, part_size):
        return fp.read(part_size)
