from __future__ import annotations

import os
import re
from typing import TYPE_CHECKING

from pymediainfo import MediaInfo

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

if TYPE_CHECKING:
    from datetime import datetime


class SendPaidMedia:
    async def send_paid_media(
        self: pyrogram.Client,
        chat_id: int | str,
        stars_amount: int,
        media: list[
            types.InputMediaAnimation
            | types.InputMediaPhoto
            | types.InputMediaVideo
        ],
        caption: str = "",
        caption_entities: list[types.MessageEntity] | None = None,
        parse_mode: enums.ParseMode | None = None,
        disable_notification: bool | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
        invert_media: bool | None = None,
    ) -> types.Message:
        """Send paid media.
        Only for channels.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel (in the format @channelusername).

            stars_amount (``int``):
                Amount of stars.

            media (List of :obj:`~pyrogram.types.InputMediaAnimation` | :obj:`~pyrogram.types.InputMediaPhoto` | :obj:`~pyrogram.types.InputMediaVideo`):
                A list of media to send.

            caption (``str``, *optional*):
                Media caption, 0-1024 characters.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                Special entities that appear in the caption, which can be specified instead of parse_mode.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your bot's message.

            disable_notification (``bool``, *optional*):
                Sends the message silently. Users will receive a notification with no sound.

            schedule_date (:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent. Pass a :obj:`~datetime.datetime` object.

            protect_content (``bool``, *optional*):
                Protect content from being forwarded.

            invert_media (``bool``, *optional*):
                Invert the media.

        Example:
            .. code-block:: python

                app.send_paid_media(
                    chat_id="pyrogram",
                    stars_amount=100,
                    media=[
                        types.InputMediaPhoto("/path/to/photo.jpg"),
                        types.InputMediaVideo("video_file_id")
                    ],
                    caption="This is a paid media message."
                )
        """
        multi_media = []

        for i in media:
            if isinstance(i, types.InputMediaPhoto):
                if isinstance(i.media, str):
                    if os.path.isfile(i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedPhoto(
                                    file=await self.save_file(
                                        i.media
                                    ),
                                    spoiler=i.has_spoiler,
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaPhotoExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaPhoto(
                            id=raw.types.InputPhoto(
                                id=media.photo.id,
                                access_hash=media.photo.access_hash,
                                file_reference=media.photo.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.PHOTO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedPhoto(
                                file=await self.save_file(i.media),
                                spoiler=i.has_spoiler,
                            ),
                        )
                    )

                    media = raw.types.InputMediaPhoto(
                        id=raw.types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash,
                            file_reference=media.photo.file_reference,
                        ),
                        spoiler=i.has_spoiler,
                    )
            elif isinstance(
                i, types.InputMediaVideo | types.InputMediaAnimation
            ):
                if isinstance(i.media, str):
                    is_animation = False
                    if os.path.isfile(i.media):
                        try:
                            videoInfo = MediaInfo.parse(i.media)
                        except OSError:
                            is_animation = bool(
                                isinstance(
                                    i, types.InputMediaAnimation
                                )
                            )
                        else:
                            if not any(
                                track.track_type == "Audio"
                                for track in videoInfo.tracks
                            ):
                                is_animation = True
                        attributes = [
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True
                                if is_animation
                                else (i.supports_streaming or None),
                                duration=i.duration,
                                w=i.width,
                                h=i.height,
                            ),
                            raw.types.DocumentAttributeFilename(
                                file_name=os.path.basename(i.media)
                            ),
                        ]
                        if is_animation:
                            attributes.append(
                                raw.types.DocumentAttributeAnimated()
                            )
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaUploadedDocument(
                                    file=await self.save_file(
                                        i.media
                                    ),
                                    thumb=await self.save_file(
                                        i.thumb
                                    ),
                                    spoiler=i.has_spoiler,
                                    mime_type=self.guess_mime_type(
                                        i.media
                                    )
                                    or "video/mp4",
                                    nosound_video=is_animation,
                                    attributes=attributes,
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    elif re.match("^https?://", i.media):
                        media = await self.invoke(
                            raw.functions.messages.UploadMedia(
                                peer=await self.resolve_peer(chat_id),
                                media=raw.types.InputMediaDocumentExternal(
                                    url=i.media, spoiler=i.has_spoiler
                                ),
                            )
                        )

                        media = raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=media.document.id,
                                access_hash=media.document.access_hash,
                                file_reference=media.document.file_reference,
                            ),
                            spoiler=i.has_spoiler,
                        )
                    else:
                        media = utils.get_input_media_from_file_id(
                            i.media, FileType.VIDEO
                        )
                else:
                    media = await self.invoke(
                        raw.functions.messages.UploadMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=raw.types.InputMediaUploadedDocument(
                                file=await self.save_file(i.media),
                                thumb=await self.save_file(i.thumb),
                                spoiler=i.has_spoiler,
                                mime_type=self.guess_mime_type(
                                    getattr(
                                        i.media, "name", "video.mp4"
                                    )
                                )
                                or "video/mp4",
                                attributes=[
                                    raw.types.DocumentAttributeVideo(
                                        supports_streaming=i.supports_streaming
                                        or None,
                                        duration=i.duration,
                                        w=i.width,
                                        h=i.height,
                                    ),
                                    raw.types.DocumentAttributeFilename(
                                        file_name=getattr(
                                            i.media,
                                            "name",
                                            "video.mp4",
                                        )
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
                        ),
                        spoiler=i.has_spoiler,
                    )
            else:
                raise ValueError(
                    f"{i.__class__.__name__} is not a supported type for send_paid_media"
                )
            multi_media.append(media)

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaPaidMedia(
                stars_amount=stars_amount, extended_media=multi_media
            ),
            silent=disable_notification or None,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            invert_media=invert_media,
            **await utils.parse_text_entities(
                self, caption, parse_mode, caption_entities
            ),
        )
        r = await self.invoke(rpc, sleep_threshold=60)

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[
                    m.message
                    for m in filter(
                        lambda u: isinstance(
                            u,
                            raw.types.UpdateNewMessage
                            | raw.types.UpdateNewChannelMessage
                            | raw.types.UpdateNewScheduledMessage
                            | raw.types.UpdateBotNewBusinessMessage,
                        ),
                        r.updates,
                    )
                ],
                users=r.users,
                chats=r.chats,
            ),
        )
