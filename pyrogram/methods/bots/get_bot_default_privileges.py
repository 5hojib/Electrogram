from typing import Optional

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetBotDefaultPrivileges:
    async def get_bot_default_privileges(
        self: "pyrogram.Client",
        for_channels: bool = None
    ) -> Optional["types.ChatPrivileges"]:
        bot_info = await self.invoke(
            raw.functions.users.GetFullUser(
                id=raw.types.InputUserSelf()
            )
        )

        field = "bot_broadcast_admin_rights" if for_channels else "bot_group_admin_rights"

        admin_rights = getattr(bot_info.full_user, field)

        return types.ChatPrivileges._parse(admin_rights) if admin_rights else None
