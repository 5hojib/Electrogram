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
        async with self.save_file_semaphore:
            if path is None:
                return None

            part_size = 512 * 1024

            if isinstance(path, str | PurePath):
                fp = Path(path).open("rb")
            elif isinstance(path, io.IOBase):
                fp = path
            else:
                raise ValueError(
                    "Invalid file. Expected a file path as string or a binary (not text) file pointer"
                )

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

            file_total_parts = int(math.ceil(file_size / part_size))
            is_big = file_size > 10 * 1024 * 1024
            workers_count = min(
                8, (file_size // (100 * 1024 * 1024)) + 1
            )  # Max 8 workers
            is_missing_part = file_id is not None
            file_id = file_id or self.rnd_id()
            md5_sum = md5() if not is_big and not is_missing_part else None

            async def worker(session, queue) -> None:
                while True:
                    data = await queue.get()
                    if data is None:
                        return
                    try:
                        await session.invoke(data)
                    except Exception as e:
                        log.exception(e)

            # Create multiple sessions for parallel uploads
            async def session_factory():
                return Session(
                    self,
                    await self.storage.dc_id(),
                    await self.storage.auth_key(),
                    await self.storage.test_mode(),
                    is_media=True,
                )

            sessions = [await session_factory() for _ in range(workers_count)]
            workers = []
            queue = asyncio.Queue(maxsize=workers_count)

            try:
                # Start all sessions
                for session in sessions:
                    await session.start()
                    workers.append(self.loop.create_task(worker(session, queue)))

                fp.seek(part_size * file_part)

                while True:
                    chunk = fp.read(part_size)
                    if not chunk:
                        if not is_big and not is_missing_part:
                            md5_sum = "".join(
                                [hex(i)[2:].zfill(2) for i in md5_sum.digest()]
                            )
                        break

                    if is_big:
                        rpc = raw.functions.upload.SaveBigFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            file_total_parts=file_total_parts,
                            bytes=chunk,
                        )
                    else:
                        rpc = raw.functions.upload.SaveFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            bytes=chunk,
                        )

                    await queue.put(rpc)

                    if is_missing_part:
                        return None

                    if not is_big and not is_missing_part:
                        md5_sum.update(chunk)

                    file_part += 1

                    if progress:
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
                log.exception(e)
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

                for session in sessions:
                    await session.stop()

                if isinstance(path, str | PurePath):
                    fp.close()
