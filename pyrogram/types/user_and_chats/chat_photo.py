from typing import Union

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class ChatPhoto(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        small_file_id: str,
        small_photo_unique_id: str,
        big_file_id: str,
        big_photo_unique_id: str,
        has_animation: bool,
        is_personal: bool,
        minithumbnail: "types.StrippedThumbnail" = None
    ):
        super().__init__(client)

        self.small_file_id = small_file_id
        self.small_photo_unique_id = small_photo_unique_id
        self.big_file_id = big_file_id
        self.big_photo_unique_id = big_photo_unique_id
        self.has_animation = has_animation
        self.is_personal = is_personal
        self.minithumbnail = minithumbnail

    @staticmethod
    def _parse(
        client,
        chat_photo: Union["raw.types.UserProfilePhoto", "raw.types.ChatPhoto"],
        peer_id: int,
        peer_access_hash: int
    ):
        if not isinstance(chat_photo, (raw.types.UserProfilePhoto, raw.types.ChatPhoto)):
            return None

        return ChatPhoto(
            small_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=chat_photo.photo_id,
                access_hash=0,
                volume_id=0,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_SMALL,
                local_id=0,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash
            ).encode(),
            small_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=chat_photo.photo_id
            ).encode(),
            big_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=chat_photo.photo_id,
                access_hash=0,
                volume_id=0,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_BIG,
                local_id=0,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash
            ).encode(),
            big_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=chat_photo.photo_id
            ).encode(),
            has_animation=chat_photo.has_video,
            is_personal=getattr(chat_photo, "personal", False),
            minithumbnail=types.StrippedThumbnail(
                data=chat_photo.stripped_thumb
            ) if chat_photo.stripped_thumb else None,
            client=client
        )
