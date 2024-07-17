import io
import os
import re
from typing import Union, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from pyrogram.file_id import FileType


class EditMessageMedia:
    async def edit_message_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        file_name: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        invert_media: bool = False,
    ) -> "types.Message":
        caption = media.caption
        parse_mode = parse_mode

        message, entities = None, None

        if caption is not None:
            message, entities = (await self.parser.parse(caption, parse_mode)).values()

        if isinstance(media, types.InputMediaPhoto):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedPhoto(
                            file=await self.save_file(media.media),
                            spoiler=media.has_spoiler,
                        ),
                    )
                )

                media = raw.types.InputMediaPhoto(
                    id=raw.types.InputPhoto(
                        id=uploaded_media.photo.id,
                        access_hash=uploaded_media.photo.access_hash,
                        file_reference=uploaded_media.photo.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaPhotoExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.PHOTO)
        elif isinstance(media, types.InputMediaVideo):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=media.supports_streaming or None,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height,
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                            ],
                        ),
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.VIDEO)
        elif isinstance(media, types.InputMediaAudio):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "audio/mpeg",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeAudio(
                                    duration=media.duration,
                                    performer=media.performer,
                                    title=media.title,
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                            ],
                        ),
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference,
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(url=media.media)
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.AUDIO)
        elif isinstance(media, types.InputMediaAnimation):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                uploaded_media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=await self.save_file(media.thumb),
                            spoiler=media.has_spoiler,
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeVideo(
                                    supports_streaming=True,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height,
                                ),
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                ),
                                raw.types.DocumentAttributeAnimated(),
                            ],
                        ),
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=uploaded_media.document.id,
                        access_hash=uploaded_media.document.access_hash,
                        file_reference=uploaded_media.document.file_reference,
                    ),
                    spoiler=media.has_spoiler,
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media, spoiler=media.has_spoiler
                )
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, FileType.ANIMATION
                )
        elif isinstance(media, types.InputMediaDocument):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = await self.invoke(
                    raw.functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=raw.types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media)
                            or "application/zip",
                            thumb=await self.save_file(media.thumb),
                            file=await self.save_file(media.media),
                            attributes=[
                                raw.types.DocumentAttributeFilename(
                                    file_name=file_name or os.path.basename(media.media)
                                )
                            ],
                        ),
                    )
                )

                media = raw.types.InputMediaDocument(
                    id=raw.types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=media.document.file_reference,
                    )
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(url=media.media)
            else:
                media = utils.get_input_media_from_file_id(
                    media.media, FileType.DOCUMENT
                )

        r = await self.invoke(
            raw.functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                media=media,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                message=message,
                entities=entities,
                invert_media=invert_media,
            )
        )

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateEditMessage, raw.types.UpdateEditChannelMessage)
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )
