from typing import Union, Iterable

import pyrogram
from pyrogram import raw


class DeleteMessages:
    async def delete_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True,
    ) -> int:
        peer = await self.resolve_peer(chat_id)
        message_ids = (
            list(message_ids) if not isinstance(message_ids, int) else [message_ids]
        )

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteMessages(channel=peer, id=message_ids)
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteMessages(id=message_ids, revoke=revoke)
            )

        return r.pts_count
