from typing import List, Match

import pyrogram
from pyrogram import raw
from pyrogram import types, enums
from ..object import Object
from ..update import Update


class InlineQuery(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        from_user: "types.User",
        query: str,
        offset: str,
        chat_type: "enums.ChatType",
        location: "types.Location" = None,
        matches: List[Match] = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.chat_type = chat_type
        self.location = location
        self.matches = matches

    @staticmethod
    def _parse(client, inline_query: raw.types.UpdateBotInlineQuery, users: dict) -> "InlineQuery":
        peer_type = inline_query.peer_type
        chat_type = None

        if isinstance(peer_type, raw.types.InlineQueryPeerTypeSameBotPM):
            chat_type = enums.ChatType.BOT
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypePM):
            chat_type = enums.ChatType.PRIVATE
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeChat):
            chat_type = enums.ChatType.GROUP
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeMegagroup):
            chat_type = enums.ChatType.SUPERGROUP
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeBroadcast):
            chat_type = enums.ChatType.CHANNEL

        return InlineQuery(
            id=str(inline_query.query_id),
            from_user=types.User._parse(client, users[inline_query.user_id]),
            query=inline_query.query,
            offset=inline_query.offset,
            chat_type=chat_type,
            location=types.Location(
                longitude=inline_query.geo.long,
                latitude=inline_query.geo.lat,
                client=client
            ) if inline_query.geo else None,
            client=client
        )

    async def answer(
        self,
        results: List["types.InlineQueryResult"],
        cache_time: int = 300,
        is_gallery: bool = False,
        is_personal: bool = False,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        return await self._client.answer_inline_query(
            inline_query_id=self.id,
            results=results,
            cache_time=cache_time,
            is_gallery=is_gallery,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter
        )
