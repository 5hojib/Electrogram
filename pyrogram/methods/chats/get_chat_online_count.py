from typing import Union

import pyrogram
from pyrogram import raw


class GetChatOnlineCount:
    async def get_chat_online_count(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> int:
        return (
            await self.invoke(
                raw.functions.messages.GetOnlines(peer=await self.resolve_peer(chat_id))
            )
        ).onlines
