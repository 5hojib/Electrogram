from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetSendAsChats:
    async def get_send_as_chats(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> List["types.Chat"]:
        r = await self.invoke(
            raw.functions.channels.GetSendAs(peer=await self.resolve_peer(chat_id))
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        send_as_chats = types.List()

        for p in r.peers:
            if isinstance(p.peer, raw.types.PeerUser):
                send_as_chats.append(
                    types.Chat._parse_chat(self, users[p.peer.user_id])
                )
            else:
                send_as_chats.append(
                    types.Chat._parse_chat(self, chats[p.peer.channel_id])
                )

        return send_as_chats
