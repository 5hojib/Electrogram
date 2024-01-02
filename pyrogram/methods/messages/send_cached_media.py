from datetime import datetime
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils


class SendCachedMedia:
    async def send_cached_media(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        file_id: str,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
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
        ] = None
    ) -> Optional["types.Message"]:
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

        media = utils.get_input_media_from_file_id(file_id)
        media.spoiler = has_spoiler

        media = utils.get_input_media_from_file_id(file_id)
        media.spoiler = has_spoiler

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
