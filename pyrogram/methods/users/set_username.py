from typing import Optional

import pyrogram
from pyrogram import raw


class SetUsername:
    async def set_username(self: "pyrogram.Client", username: Optional[str]) -> bool:
        return bool(
            await self.invoke(
                raw.functions.account.UpdateUsername(username=username or "")
            )
        )
