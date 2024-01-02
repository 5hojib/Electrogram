from typing import Union, List, AsyncGenerator, Optional

import pyrogram
from pyrogram import raw, types, utils, enums


async def get_chunk(
    client,
    chat_id: Union[int, str],
    query: str = "",
    filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
    offset: int = 0,
    limit: int = 100,
    from_user: Union[int, str] = None
) -> List["types.Message"]:
    r = await client.invoke(
        raw.functions.messages.Search(
            peer=await client.resolve_peer(chat_id),
            q=query,
            filter=filter.value(),
            min_date=0,
            max_date=0,
            offset_id=0,
            add_offset=offset,
            limit=limit,
            min_id=0,
            max_id=0,
            from_id=(
                await client.resolve_peer(from_user)
                if from_user
                else None
            ),
            hash=0
        ),
        sleep_threshold=60
    )

    return await utils.parse_messages(client, r, replies=0)


class SearchMessages:
    async def search_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        offset: int = 0,
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
        limit: int = 0,
        from_user: Union[int, str] = None
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await get_chunk(
                client=self,
                chat_id=chat_id,
                query=query,
                filter=filter,
                offset=offset,
                limit=limit,
                from_user=from_user
            )

            if not messages:
                return

            offset += len(messages)

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return
