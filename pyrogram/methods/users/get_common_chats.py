from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetCommonChats:
    async def get_common_chats(
        self: "pyrogram.Client",
        user_id: Union[int, str]
    ) -> List["types.Chat"]:
        peer = await self.resolve_peer(user_id)

        if isinstance(peer, raw.types.InputPeerUser):
            r = await self.invoke(
                raw.functions.messages.GetCommonChats(
                    user_id=peer,
                    max_id=0,
                    limit=100,
                )
            )

            return types.List([types.Chat._parse_chat(self, x) for x in r.chats])

        raise ValueError(f'The user_id "{user_id}" doesn\'t belong to a user')
