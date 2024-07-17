from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import enums


class UpdateColor:
    async def update_color(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        color: Union["enums.ReplyColor", "enums.ProfileColor"],
        background_emoji_id: int = None,
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            r = await self.invoke(
                raw.functions.account.UpdateColor(
                    for_profile=isinstance(color, enums.ProfileColor),
                    color=color.value,
                    background_emoji_id=background_emoji_id,
                )
            )
        else:
            r = await self.invoke(
                raw.functions.channels.UpdateColor(
                    channel=peer,
                    color=color.value,
                    background_emoji_id=background_emoji_id,
                )
            )

        return bool(r)
