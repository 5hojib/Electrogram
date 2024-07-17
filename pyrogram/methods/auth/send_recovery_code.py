import logging

import pyrogram
from pyrogram import raw

log = logging.getLogger(__name__)


class SendRecoveryCode:
    async def send_recovery_code(
        self: "pyrogram.Client",
    ) -> str:
        return (
            await self.invoke(raw.functions.auth.RequestPasswordRecovery())
        ).email_pattern
