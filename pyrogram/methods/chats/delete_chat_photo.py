from typing import Union

import pyrogram
from pyrogram import raw


class DeleteChatPhoto:
    async def delete_chat_photo(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id, photo=raw.types.InputChatPhotoEmpty()
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditPhoto(
                    channel=peer, photo=raw.types.InputChatPhotoEmpty()
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
