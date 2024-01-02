import logging
from typing import Union

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class GetChatHistoryCount:
    async def get_chat_history_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> int:
        r = await self.invoke(
            raw.functions.messages.GetHistory(
                peer=await self.resolve_peer(chat_id),
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0
            )
        )

        if isinstance(r, raw.types.messages.Messages):
            return len(r.messages)
        else:
            return r.count
