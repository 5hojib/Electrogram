from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetDiscussionMessage:
    async def get_discussion_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
    ) -> "types.Message":
        r = await self.invoke(
            raw.functions.messages.GetDiscussionMessage(
                peer=await self.resolve_peer(chat_id), msg_id=message_id
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        return await types.Message._parse(self, r.messages[0], users, chats)
