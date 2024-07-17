from typing import Union

import pyrogram
from pyrogram import raw, types


class PinChatMessage:
    async def pin_chat_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        disable_notification: bool = False,
        both_sides: bool = False,
    ) -> "types.Message":
        r = await self.invoke(
            raw.functions.messages.UpdatePinnedMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                silent=disable_notification or None,
                pm_oneside=not both_sides or None,
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        for i in r.updates:
            if isinstance(
                i, (raw.types.UpdateNewMessage, raw.types.UpdateNewChannelMessage)
            ):
                return await types.Message._parse(self, i.message, users, chats)
