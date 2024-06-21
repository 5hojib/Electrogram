from datetime import datetime
from typing import List, Union, Optional

import pyrogram
from pyrogram import enums, raw, utils, types


class SendContact:
    async def send_contact(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        phone_number: str,
        first_name: str,
        last_name: str = None,
        vcard: str = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        reply_to_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        message_effect_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode
        )

        rpc = raw.functions.messages.SendMedia(
            peer=await self.resolve_peer(chat_id),
            media=raw.types.InputMediaContact(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name or "",
                vcard=vcard or ""
            ),
            message="",
            silent=disable_notification or None,
            reply_to=reply_to,
            random_id=self.rnd_id(),
            schedule_date=utils.datetime_to_timestamp(schedule_date),
            noforwards=protect_content,
            reply_markup=await reply_markup.write(self) if reply_markup else None,
            effect=message_effect_id
        )
        r = await self.invoke(rpc)

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
