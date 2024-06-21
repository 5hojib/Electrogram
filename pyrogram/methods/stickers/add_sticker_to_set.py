import os
import re

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.file_id import FileId

class AddStickerToSet:
    async def add_sticker_to_set(
        self: "pyrogram.Client",
        set_short_name: str,
        sticker: str,
        emoji: str = "🤔",
    ) -> "types.StickerSet":
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
            raw.functions.stickers.AddStickerToSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=set_short_name),
                sticker=raw.types.InputStickerSetItem(
                    document=media,
                    emoji=emoji
                )
            )
        )

        return types.StickerSet._parse(r.set)
