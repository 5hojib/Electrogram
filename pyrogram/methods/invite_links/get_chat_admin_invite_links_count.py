from typing import Union

import pyrogram
from pyrogram import raw


class GetChatAdminInviteLinksCount:
    async def get_chat_admin_invite_links_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        revoked: bool = False,
    ) -> int:
        r = await self.invoke(
            raw.functions.messages.GetExportedChatInvites(
                peer=await self.resolve_peer(chat_id),
                admin_id=await self.resolve_peer(admin_id),
                limit=1,
                revoked=revoked,
            )
        )

        return r.count
