from __future__ import annotations

import pyrogram
from pyrogram import raw


class ResetSession:
    async def reset_session(self: pyrogram.Client, id: int) -> bool:
        """Log out an active authorized session by its hash.
        .. include:: /_includes/usable-by/users.rst
        Parameters:
            id (``int``):
                Session identifier.

        Returns:
            ``bool``: On success, in case the session is destroyed, True is returned. Otherwise, False is returned.
        """
        return await self.invoke(raw.functions.account.ResetAuthorization(hash=id))
