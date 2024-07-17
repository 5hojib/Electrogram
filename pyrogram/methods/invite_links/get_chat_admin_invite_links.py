from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetChatAdminInviteLinks:
    async def get_chat_admin_invite_links(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        revoked: bool = False,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.ChatInviteLink", None]]:
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = None
        offset_link = None

        while True:
            r = await self.invoke(
                raw.functions.messages.GetExportedChatInvites(
                    peer=await self.resolve_peer(chat_id),
                    admin_id=await self.resolve_peer(admin_id),
                    limit=limit,
                    revoked=revoked,
                    offset_date=offset_date,
                    offset_link=offset_link,
                )
            )

            if not r.invites:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.invites[-1].date
            offset_link = r.invites[-1].link

            for i in r.invites:
                yield types.ChatInviteLink._parse(self, i, users)

                current += 1

                if current >= total:
                    return
