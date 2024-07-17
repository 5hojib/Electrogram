from typing import Union

import pyrogram
from pyrogram import raw


class DeleteSupergroup:
    async def delete_supergroup(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> bool:
        await self.invoke(
            raw.functions.channels.DeleteChannel(
                channel=await self.resolve_peer(chat_id)
            )
        )

        return True
