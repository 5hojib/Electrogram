import os
from datetime import datetime
from typing import List, Union, BinaryIO, Optional, Callable

import pyrogram
from pyrogram import StopTransmission
from pyrogram import enums
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType


class SendVideoNote:
    async def send_video_note(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        video_note: Union[str, BinaryIO],
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        ttl_seconds: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> Optional["types.Message"]:
        file = None

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_story_id=reply_to_story_id,
            message_thread_id=message_thread_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode
        )

        try:
            if isinstance(video_note, str):
                if os.path.isfile(video_note):
                    thumb = await self.save_file(thumb)
                    file = await self.save_file(video_note, progress=progress, progress_args=progress_args)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video_note) or "video/mp4",
                        file=file,
                        thumb=thumb,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                round_message=True,
                                duration=duration,
                                w=length,
                                h=length
                            )
                        ],
                        ttl_seconds=ttl_seconds
                    )
                else:
                    media = utils.get_input_media_from_file_id(video_note, FileType.VIDEO_NOTE)
            else:
                thumb = await self.save_file(thumb)
                file = await self.save_file(video_note, progress=progress, progress_args=progress_args)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(video_note.name) or "video/mp4",
                    file=file,
                    thumb=thumb,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            round_message=True,
                            duration=duration,
                            w=length,
                            h=length
                        )
                    ]
                )

            while True:
                try:
                    r = await self.invoke(
                        raw.functions.messages.SendMedia(
                            peer=await self.resolve_peer(chat_id),
                            media=media,
                            silent=disable_notification or None,
                            reply_to=reply_to,
                            random_id=self.rnd_id(),
                            schedule_date=utils.datetime_to_timestamp(schedule_date),
                            noforwards=protect_content,
                            reply_markup=await reply_markup.write(self) if reply_markup else None,
                            message=""
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(video_note, file_id=file.id, file_part=e.value)
                else:
                    for i in r.updates:
                        if isinstance(i, (raw.types.UpdateNewMessage,
                                          raw.types.UpdateNewChannelMessage,
                                          raw.types.UpdateNewScheduledMessage)):
                            return await types.Message._parse(
                                self, i.message,
                                {i.id: i for i in r.users},
                                {i.id: i for i in r.chats},
                                is_scheduled=isinstance(i, raw.types.UpdateNewScheduledMessage)
                            )
        except StopTransmission:
            return None
