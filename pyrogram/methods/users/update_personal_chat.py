import pyrogram
from pyrogram import raw

from typing import Union


class UpdatePersonalChat:
    async def update_personal_chat(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> bool:
        chat = await self.resolve_peer(chat_id)
        r = await self.invoke(raw.functions.account.UpdatePersonalChannel(channel=chat))
        if r:
            return True
        return False
