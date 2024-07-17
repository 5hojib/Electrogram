import pyrogram
from pyrogram import raw, enums


class SearchGlobalCount:
    async def search_global_count(
        self: "pyrogram.Client",
        query: str = "",
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
    ) -> int:
        r = await self.invoke(
            raw.functions.messages.SearchGlobal(
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1,
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)
