from __future__ import annotations

import asyncio
import functools
import inspect
import io
import logging
import math
from hashlib import md5
from pathlib import Path, PurePath
from typing import TYPE_CHECKING, BinaryIO

import pyrogram
from pyrogram import StopTransmissionError, raw
from pyrogram.session import Session

if TYPE_CHECKING:
    from collections.abc import Callable

log = logging.getLogger(__name__)

class SaveFile:
    async def save_file(
        self: pyrogram.Client,
        path: str | BinaryIO,
        file_id: int | None = None,
        file_part: int = 0,
        progress: Callable | None = None,
        progress_args: tuple = (),
    ):
        """Upload a file onto Telegram servers, without actually sending the message to anyone.
        Useful whenever an InputFile type is required.

        Parameters:
            path (``str`` | ``BinaryIO``):
                The path of the file you want to upload or a binary file-like object.

            file_id (``int``, *optional*):
                File ID to resume an upload.

            file_part (``int``, *optional*):
                The file part to resume from if a previous upload was interrupted.

            progress (``Callable``, *optional*):
                Callback function for progress updates.

            progress_args (``tuple``, *optional*):
                Extra arguments for the progress callback function.

        Returns:
            ``InputFile`` or ``InputFileBig`` object on success.
        """
        async with self.save_file_semaphore:
            if path is None:
                return None

            async def worker(session) -> None:
                while True:
                    data = await queue.get()
                    if data is None:
                        return
                    for attempt in range(3):
                        try:
                            await session.invoke(data)
                            break
                        except Exception as e:
                            log.warning("Retrying part due to error: %s", e)
                            await asyncio.sleep(2**attempt)
                    else:
                        log.error("Failed to upload part after 3 attempts")

            def create_rpc(chunk, file_part, is_big, file_id, file_total_parts):
                if is_big:
                    return raw.functions.upload.SaveBigFilePart(
                        file_id=file_id,
                        file_part=file_part,
                        file_total_parts=file_total_parts,
                        bytes=chunk,
                    )
                return raw.functions.upload.SaveFilePart(
                    file_id=file_id, file_part=file_part, bytes=chunk
                )

            part_size = 512 * 1024
            queue = asyncio.Queue(16)

            with (
                Path(path).open("rb", buffering=4096)
                if isinstance(path, str | PurePath)
                else path
            ) as fp:
                file_name = getattr(fp, "name", "file.jpg")
                fp.seek(0, io.SEEK_END)
                file_size = fp.tell()
                fp.seek(0)

                if file_size == 0:
                    raise ValueError("File size equals to 0 B")

                file_size_limit_mib = 4000 if self.me.is_premium else 2000

                if file_size > file_size_limit_mib * 1024 * 1024:
                    raise ValueError(
                        f"Can't upload files bigger than {file_size_limit_mib} MiB"
                    )

                file_total_parts = math.ceil(file_size / part_size)
                is_big = file_size > 100 * 1024 * 1024
                pool_size = 2 if is_big else 1
                workers_count = 10 if is_big else 1
                is_missing_part = file_id is not None
                file_id = file_id or self.rnd_id()
                md5_sum = md5() if not is_big and not is_missing_part else None

                pool = [
                    Session(
                        self,
                        await self.storage.dc_id(),
                        await self.storage.auth_key(),
                        await self.storage.test_mode(),
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
                                md5_sum = md5_sum.hexdigest()
                            break

                        await queue.put(
                            create_rpc(
                                chunk, file_part, is_big, file_id, file_total_parts
                            )
                        )

                        if not is_missing_part:
                            file_part += 1  # Ensure this only increments after success

                        if not is_big and not is_missing_part:
                            md5_sum.update(chunk)

                        # Progress handling
                        if progress and file_total_parts > 10 and file_part % (file_total_parts // 10) == 0:
                            func = functools.partial(
                                progress,
                                min(file_part * part_size, file_size),
                                file_size,
                                *progress_args,
                            )

                            if inspect.iscoroutinefunction(progress):
                                await func()
                            else:
                                await self.loop.run_in_executor(self.executor, func)

                except StopTransmissionError:
                    raise
                except Exception as e:
                    log.error(
                        "Error during file upload at part %s: %s", file_part, e
                    )
                else:
                    if is_big:
                        return raw.types.InputFileBig(
                            id=file_id,
                            parts=file_total_parts,
                            name=file_name,
                        )
                    return raw.types.InputFile(
                        id=file_id,
                        parts=file_total_parts,
                        name=file_name,
                        md5_checksum=md5_sum,
                    )
                finally:
                    for _ in workers:
                        await queue.put(None)

                    await asyncio.gather(*workers)

                    for session in pool:
                        await session.stop()

    async def preload(self, fp, part_size):
        return fp.read(part_size)