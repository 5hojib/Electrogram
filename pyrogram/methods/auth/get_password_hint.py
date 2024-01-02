import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class GetPasswordHint:
    async def get_password_hint(
        self: "pyrogram.Client",
    ) -> str:
        return (await self.invoke(raw.functions.account.GetPassword())).hint
