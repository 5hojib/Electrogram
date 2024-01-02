import os
import re
from datetime import datetime
from typing import Union, BinaryIO, List, Optional, Callable

import pyrogram
from pyrogram import StopTransmission, enums
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import FilePartMissing
from pyrogram.file_id import FileType


class SendVoice:
    async def send_voice(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        voice: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_chat_id: int = None,
        quote_text: str = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
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

        reply_to = None
        reply_to_chat = None
        if reply_to_message_id or message_thread_id:
            if reply_to_chat_id is not None:
                reply_to_chat = await self.resolve_peer(reply_to_chat_id)
            reply_to = types.InputReplyToMessage(
                reply_to_message_id=reply_to_message_id,
                message_thread_id=message_thread_id,
                reply_to_chat=reply_to_chat,
                quote_text=quote_text
            )
        if reply_to_story_id:
            user_id = await self.resolve_peer(chat_id)
            reply_to = types.InputReplyToStory(user_id=user_id, story_id=reply_to_story_id)

        try:
            if isinstance(voice, str):
                if os.path.isfile(voice):
                    file = await self.save_file(voice, progress=progress, progress_args=progress_args)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(voice) or "audio/mpeg",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeAudio(
                                voice=True,
                                duration=duration
                            )
                        ]
                    )
                elif re.match("^https?://", voice):
                    media = raw.types.InputMediaDocumentExternal(
                        url=voice
                    )
                else:
                    media = utils.get_input_media_from_file_id(voice, FileType.VOICE)
            else:
                file = await self.save_file(voice, progress=progress, progress_args=progress_args)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(voice.name) or "audio/mpeg",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeAudio(
                            voice=True,
                            duration=duration
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
                            **await utils.parse_text_entities(self, caption, parse_mode, caption_entities)
                        )
                    )
                except FilePartMissing as e:
                    await self.save_file(voice, file_id=file.id, file_part=e.value)
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
