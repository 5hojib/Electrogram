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


class Video(Object):
    """A video file.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        supports_streaming (``bool``, *optional*):
            True, if the video was uploaded with streaming support.

        ttl_seconds (``int``. *optional*):
            Time-to-live seconds, for secret photos.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the video was sent.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        duration: int,
        file_name: str | None = None,
        mime_type: str | None = None,
        file_size: int | None = None,
        supports_streaming: bool | None = None,
        ttl_seconds: int | None = None,
        date: datetime | None = None,
        thumbs: list[types.Thumbnail] | None = None,
    ) -> None:
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.supports_streaming = supports_streaming
        self.ttl_seconds = ttl_seconds
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        video: raw.types.Document,
        video_attributes: raw.types.DocumentAttributeVideo,
        file_name: str,
        ttl_seconds: int | None = None,
    ) -> Video:
        return Video(
            file_id=FileId(
                file_type=FileType.VIDEO,
                dc_id=video.dc_id,
                media_id=video.id,
                access_hash=video.access_hash,
                file_reference=video.file_reference,
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=video.id,
            ).encode(),
            width=video_attributes.w,
            height=video_attributes.h,
            duration=video_attributes.duration,
            file_name=file_name,
            mime_type=video.mime_type,
            supports_streaming=video_attributes.supports_streaming,
            file_size=video.size,
            date=utils.timestamp_to_datetime(video.date),
            ttl_seconds=ttl_seconds,
            thumbs=types.Thumbnail._parse(client, video),
            client=client,
        )
