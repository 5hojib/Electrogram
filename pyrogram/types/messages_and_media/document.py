from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.file_id import (
    FileId,
    FileType,
    FileUniqueId,
    FileUniqueType,
)
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class Document(Object):
    """A generic file (as opposed to photos, voice messages, audio files, ...).

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        file_name (``str``, *optional*):
            Original filename as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the document was sent.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Document thumbnails as defined by sender.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        file_id: str,
        file_unique_id: str,
        file_name: str | None = None,
        mime_type: str | None = None,
        file_size: int | None = None,
        date: datetime | None = None,
        thumbs: list[types.Thumbnail] | None = None,
    ) -> None:
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, document: raw.types.Document, file_name: str) -> Document:
        return Document(
            file_id=FileId(
                file_type=FileType.DOCUMENT,
                dc_id=document.dc_id,
                media_id=document.id,
                access_hash=document.access_hash,
                file_reference=document.file_reference,
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=document.id,
            ).encode(),
            file_name=file_name,
            mime_type=document.mime_type,
            file_size=document.size,
            date=utils.timestamp_to_datetime(document.date),
            thumbs=types.Thumbnail._parse(client, document),
            client=client,
        )
