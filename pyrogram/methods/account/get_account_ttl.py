from __future__ import annotations

import pyrogram
from pyrogram import raw


class GetAccountTTL:
    async def get_account_ttl(
        self: pyrogram.Client,
    ) -> int:
        """Get days to live of account.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``int``: Time to live in days of the current account.

        Example:
            .. code-block:: python

                # Get ttl in days
                await app.get_account_ttl()
        """
        r = await self.invoke(raw.functions.account.GetAccountTTL())

        return r.days
