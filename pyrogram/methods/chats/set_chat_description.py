from typing import Union

import pyrogram
from pyrogram import raw


class SetChatDescription:
    async def set_chat_description(
        self: "pyrogram.Client", chat_id: Union[int, str], description: str
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            await self.invoke(
                raw.functions.messages.EditChatAbout(peer=peer, about=description)
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
