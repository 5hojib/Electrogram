from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import raw, utils
from pyrogram import types


class CreateChatInviteLink:
    async def create_chat_invite_link(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        name: str = None,
        expire_date: datetime = None,
        member_limit: int = None,
        creates_join_request: bool = None,
    ) -> "types.ChatInviteLink":
        r = await self.invoke(
            raw.functions.messages.ExportChatInvite(
                peer=await self.resolve_peer(chat_id),
                expire_date=utils.datetime_to_timestamp(expire_date),
                usage_limit=member_limit,
                title=name,
                request_needed=creates_join_request,
            )
        )

        return types.ChatInviteLink._parse(self, r)
