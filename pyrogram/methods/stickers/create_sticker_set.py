import os
import re
from typing import Union, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.file_id import FileId


class CreateStickerSet:
    async def create_sticker_set(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        title: str,
        short_name: str,
        sticker: str,
        emoji: str = "🤔",
        masks: bool = None
    ) -> Optional["types.Message"]:
        file = None

        if isinstance(sticker, str):
            if os.path.isfile(sticker) or re.match("^https?://", sticker):
                raise ValueError(f"file_id is invalid!")
            else:
                decoded = FileId.decode(sticker)
                media = raw.types.InputDocument(
                    id=decoded.media_id,
                    access_hash=decoded.access_hash,
                    file_reference=decoded.file_reference
                )
        else:
            raise ValueError(f"file_id is invalid!")

        r = await self.invoke(
            raw.functions.stickers.CreateStickerSet(
                user_id=await self.resolve_peer(user_id),
                title=title,
                short_name=short_name,
                stickers=[
                    raw.types.InputStickerSetItem(
                        document=media,
                        emoji=emoji
                    )
                ],
                masks=masks
            )
        )

        return types.StickerSet._parse(r.set)
