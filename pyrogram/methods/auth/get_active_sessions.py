from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetActiveSessions:
    async def get_active_sessions(
        self: pyrogram.Client,
    ) -> types.ActiveSessions:
        """Returns all active sessions of the current user.
        .. include:: /_includes/usable-by/users.rst
        Returns:
            :obj:`~pyrogram.types.ActiveSessions`: On success, all the active sessions of the current user is returned.
        """
        r = await self.invoke(raw.functions.account.GetAuthorizations())
        return types.ActiveSessions._parse(r)
