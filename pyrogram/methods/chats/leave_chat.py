from typing import Union

import pyrogram
from pyrogram import raw


class LeaveChat:
    async def leave_chat(
        self: "pyrogram.Client", chat_id: Union[int, str], delete: bool = False
    ):
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            return await self.invoke(
                raw.functions.channels.LeaveChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )
        elif isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id, user_id=raw.types.InputUserSelf()
                )
            )

            if delete:
                await self.invoke(
                    raw.functions.messages.DeleteHistory(peer=peer, max_id=0)
                )

            return r
