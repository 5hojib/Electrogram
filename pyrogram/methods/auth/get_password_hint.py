from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class GetPasswordHint:
    async def get_password_hint(
        self: pyrogram.Client,
    ) -> str:
        """Get your Two-Step Verification password hint.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``str``: On success, the password hint as string is returned.
        """
        return (await self.invoke(raw.functions.account.GetPassword())).hint
