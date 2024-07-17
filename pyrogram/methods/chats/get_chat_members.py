import logging
from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw, types, enums

log = logging.getLogger(__name__)


async def get_chunk(
    client: "pyrogram.Client",
    chat_id: Union[int, str],
    offset: int,
    filter: "enums.ChatMembersFilter",
    limit: int,
    query: str,
):
    is_queryable = filter in [
        enums.ChatMembersFilter.SEARCH,
        enums.ChatMembersFilter.BANNED,
        enums.ChatMembersFilter.RESTRICTED,
    ]

    filter = filter.value(q=query) if is_queryable else filter.value()

    r = await client.invoke(
        raw.functions.channels.GetParticipants(
            channel=await client.resolve_peer(chat_id),
            filter=filter,
            offset=offset,
            limit=limit,
            hash=0,
        ),
        sleep_threshold=60,
    )

    members = r.participants
    users = {u.id: u for u in r.users}
    chats = {c.id: c for c in r.chats}

    return [types.ChatMember._parse(client, member, users, chats) for member in members]


class GetChatMembers:
    async def get_chat_members(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        limit: int = 0,
        filter: "enums.ChatMembersFilter" = enums.ChatMembersFilter.SEARCH,
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.GetFullChat(chat_id=peer.chat_id)
            )

            members = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for member in members:
                yield types.ChatMember._parse(self, member, users, {})

            return

        current = 0
        offset = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(200, total)

        while True:
            members = await get_chunk(
                client=self,
                chat_id=chat_id,
                offset=offset,
                filter=filter,
                limit=limit,
                query=query,
            )

            if not members:
                return

            offset += len(members)

            for member in members:
                yield member

                current += 1

                if current >= total:
                    return
