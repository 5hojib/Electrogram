from typing import Union

import pyrogram
from pyrogram import raw, types


class GetChatAdminsWithInviteLinks:
    async def get_chat_admins_with_invite_links(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
    ):
        r = await self.invoke(
            raw.functions.messages.GetAdminsWithInvites(
                peer=await self.resolve_peer(chat_id)
            )
        )

        users = {i.id: i for i in r.users}

        return types.List(
            types.ChatAdminWithInviteLinks._parse(self, admin, users)
            for admin in r.admins
        )
