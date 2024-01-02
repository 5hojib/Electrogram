import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class LogOut:
    async def log_out(
        self: "pyrogram.Client",
    ):
        await self.invoke(raw.functions.auth.LogOut())
        await self.stop()
        await self.storage.delete()

        return True
