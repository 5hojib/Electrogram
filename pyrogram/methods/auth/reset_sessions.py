from __future__ import annotations

import pyrogram
from pyrogram import raw


class ResetSessions:
    async def reset_sessions(
        self: pyrogram.Client,
    ) -> bool:
        """Terminates all user's authorized sessions except for the current one.
        .. include:: /_includes/usable-by/users.rst
        Returns:
            ``bool``: On success, in case the sessions is destroyed, True is returned. Otherwise, False is returned.
        """
        return await self.invoke(raw.functions.auth.ResetAuthorizations())
