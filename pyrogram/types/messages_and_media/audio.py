from datetime import datetime
from typing import List

import pyrogram
from pyrogram import raw, utils
from pyrogram import types
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class Audio(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        duration: int,
        performer: str = None,
        title: str = None,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None,
        thumbs: List["types.Thumbnail"] = None,
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.performer = performer
        self.title = title
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        audio: "raw.types.Document",
        audio_attributes: "raw.types.DocumentAttributeAudio",
        file_name: str,
    ) -> "Audio":
        return Audio(
            file_id=FileId(
                file_type=FileType.AUDIO,
                dc_id=audio.dc_id,
                media_id=audio.id,
                access_hash=audio.access_hash,
                file_reference=audio.file_reference,
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT, media_id=audio.id
            ).encode(),
            duration=audio_attributes.duration,
            performer=audio_attributes.performer,
            title=audio_attributes.title,
            mime_type=audio.mime_type,
            file_size=audio.size,
            file_name=file_name,
            date=utils.timestamp_to_datetime(audio.date),
            thumbs=types.Thumbnail._parse(client, audio),
            client=client,
        )
