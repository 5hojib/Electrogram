from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetChatInviteLink:
    async def get_chat_invite_link(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        invite_link: str,
    ) -> "types.ChatInviteLink":
        r = await self.invoke(
            raw.functions.messages.GetExportedChatInvite(
                peer=await self.resolve_peer(chat_id), link=invite_link
            )
        )

        users = {i.id: i for i in r.users}

        return types.ChatInviteLink._parse(self, r.invite, users)
