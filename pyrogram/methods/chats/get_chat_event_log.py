from typing import Union, List, AsyncGenerator, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetChatEventLog:
    async def get_chat_event_log(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        offset_id: int = 0,
        limit: int = 0,
        filters: "types.ChatEventFilter" = None,
        user_ids: List[Union[int, str]] = None,
    ) -> Optional[AsyncGenerator["types.ChatEvent", None]]:
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        while True:
            r: raw.base.channels.AdminLogResults = await self.invoke(
                raw.functions.channels.GetAdminLog(
                    channel=await self.resolve_peer(chat_id),
                    q=query,
                    min_id=0,
                    max_id=offset_id,
                    limit=limit,
                    events_filter=filters.write() if filters else None,
                    admins=(
                        [await self.resolve_peer(i) for i in user_ids]
                        if user_ids is not None
                        else user_ids
                    ),
                )
            )

            if not r.events:
                return

            last = r.events[-1]
            offset_id = last.id

            for event in r.events:
                yield await types.ChatEvent._parse(self, event, r.users, r.chats)

                current += 1

                if current >= total:
                    return
