import asyncio
import os
from datetime import datetime
from typing import Union, Optional, Callable, BinaryIO

import pyrogram
from pyrogram import types
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES

DEFAULT_DOWNLOAD_DIR = "downloads/"


class DownloadMedia:
    async def download_media(
        self: "pyrogram.Client",
        message: Union["types.Message", "types.Story", str],
        file_name: str = DEFAULT_DOWNLOAD_DIR,
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional[Union[str, BinaryIO]]:
        available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note",
                           "new_chat_photo")

        if isinstance(message, types.Message) or isinstance(message, types.Story):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                raise ValueError("This message doesn't contain any downloadable media")
        else:
            media = message

        if isinstance(media, str):
            file_id_str = media
        else:
            file_id_str = media.file_id

        file_id_obj = FileId.decode(file_id_str)

        file_type = file_id_obj.file_type
        media_file_name = getattr(media, "file_name", "")
        file_size = getattr(media, "file_size", 0)
        mime_type = getattr(media, "mime_type", "")
        date = getattr(media, "date", None)

        directory, file_name = os.path.split(file_name)
        file_name = file_name or media_file_name or ""

        if not os.path.isabs(file_name):
            directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

        if not file_name:
            guessed_extension = self.guess_extension(mime_type)

            if file_type in PHOTO_TYPES:
                extension = ".jpg"
            elif file_type == FileType.VOICE:
                extension = guessed_extension or ".ogg"
            elif file_type in (FileType.VIDEO, FileType.ANIMATION, FileType.VIDEO_NOTE):
                extension = guessed_extension or ".mp4"
            elif file_type == FileType.DOCUMENT:
                extension = guessed_extension or ".zip"
            elif file_type == FileType.STICKER:
                extension = guessed_extension or ".webp"
            elif file_type == FileType.AUDIO:
                extension = guessed_extension or ".mp3"
            else:
                extension = ".unknown"

            file_name = "{}_{}_{}{}".format(
                FileType(file_id_obj.file_type).name.lower(),
                (date or datetime.now()).strftime("%Y-%m-%d_%H-%M-%S"),
                self.rnd_id(),
                extension
            )

        downloader = self.handle_download(
            (file_id_obj, directory, file_name, in_memory, file_size, progress, progress_args)
        )

        if block:
            return await downloader
        else:
            asyncio.get_event_loop().create_task(downloader)
