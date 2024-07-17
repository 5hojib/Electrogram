from typing import Union

import pyrogram
from pyrogram import raw, enums


class SearchMessagesCount:
    async def search_messages_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
        from_user: Union[int, str] = None,
    ) -> int:
        r = await self.invoke(
            raw.functions.messages.Search(
                peer=await self.resolve_peer(chat_id),
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=1,
                min_id=0,
                max_id=0,
                from_id=(await self.resolve_peer(from_user) if from_user else None),
                hash=0,
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
