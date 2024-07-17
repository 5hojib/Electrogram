from typing import Union, List

import pyrogram
from pyrogram import raw


class AddChatMembers:
    async def add_chat_members(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_ids: Union[Union[int, str], List[Union[int, str]]],
        forward_limit: int = 100,
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if not isinstance(user_ids, list):
            user_ids = [user_ids]

        if isinstance(peer, raw.types.InputPeerChat):
            for user_id in user_ids:
                await self.invoke(
                    raw.functions.messages.AddChatUser(
                        chat_id=peer.chat_id,
                        user_id=await self.resolve_peer(user_id),
                        fwd_limit=forward_limit,
                    )
                )
        else:
            await self.invoke(
                raw.functions.channels.InviteToChannel(
                    channel=peer,
                    users=[await self.resolve_peer(user_id) for user_id in user_ids],
                )
            )

        return True
