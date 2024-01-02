from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types, utils


class SendGame:
    async def send_game(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        game_short_name: str,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        protect_content: bool = None,
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
            message_thread_id=message_thread_id
        )

        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaGame(
                    id=raw.types.InputGameShortName(
                        bot_id=raw.types.InputUserSelf(),
                        short_name=game_short_name
                    ),
                ),
                message="",
                silent=disable_notification or None,
                reply_to=reply_to,
                random_id=self.rnd_id(),
                noforwards=protect_content,
                reply_markup=await reply_markup.write(self) if reply_markup else None
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )
