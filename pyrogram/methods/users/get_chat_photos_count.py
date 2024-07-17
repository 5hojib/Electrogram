from typing import Union

import pyrogram
from pyrogram import raw


class GetChatPhotosCount:
    async def get_chat_photos_count(
        self: "pyrogram.Client", chat_id: Union[int, str]
    ) -> int:
        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.messages.GetSearchCounters(
                    peer=peer_id,
                    filters=[raw.types.InputMessagesFilterChatPhotos()],
                )
            )

            return r[0].count
        else:
            r = await self.invoke(
                raw.functions.photos.GetUserPhotos(
                    user_id=peer_id, offset=0, max_id=0, limit=1
                )
            )

            if isinstance(r, raw.types.photos.Photos):
                return len(r.photos)
            else:
                return r.count
