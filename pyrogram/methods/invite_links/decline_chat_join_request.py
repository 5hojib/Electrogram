from typing import Union

import pyrogram
from pyrogram import raw


class DeclineChatJoinRequest:
    async def decline_chat_join_request(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: int,
    ) -> bool:
        await self.invoke(
            raw.functions.messages.HideChatJoinRequest(
                peer=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                approved=False,
            )
        )

        return True
