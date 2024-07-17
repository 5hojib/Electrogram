from typing import Union

import pyrogram
from pyrogram import raw


class ReadChatHistory:
    async def read_chat_history(
        self: "pyrogram.Client", chat_id: Union[int, str], max_id: int = 0
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            q = raw.functions.channels.ReadHistory(channel=peer, max_id=max_id)
        else:
            q = raw.functions.messages.ReadHistory(peer=peer, max_id=max_id)

        await self.invoke(q)

        return True
