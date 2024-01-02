from datetime import datetime

import pyrogram
from pyrogram import raw, utils
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class Voice(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        duration: int,
        waveform: bytes = None,
        mime_type: str = None,
        file_size: int = None,
        date: datetime = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.duration = duration
        self.waveform = waveform
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date

    @staticmethod
    def _parse(client, voice: "raw.types.Document", attributes: "raw.types.DocumentAttributeAudio") -> "Voice":
        return Voice(
            file_id=FileId(
                file_type=FileType.VOICE,
                dc_id=voice.dc_id,
                media_id=voice.id,
                access_hash=voice.access_hash,
                file_reference=voice.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=voice.id
            ).encode(),
            duration=attributes.duration,
            mime_type=voice.mime_type,
            file_size=voice.size,
            waveform=attributes.waveform,
            date=utils.timestamp_to_datetime(voice.date),
            client=client
        )
