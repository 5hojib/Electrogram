from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetCustomEmojiStickers:
    async def get_custom_emoji_stickers(
        self: "pyrogram.Client",
        custom_emoji_ids: Union[int, List[int]],
    ) -> Union["types.Sticker", List["types.Sticker"]]:
        is_list = isinstance(custom_emoji_ids, list)
        custom_emoji_ids = [custom_emoji_ids] if not is_list else custom_emoji_ids

        result = await self.invoke(
            raw.functions.messages.GetCustomEmojiDocuments(document_id=custom_emoji_ids)
        )

        stickers = pyrogram.types.List()
        for item in result:
            attributes = {type(i): i for i in item.attributes}
            sticker = await types.Sticker._parse(self, item, attributes)
            stickers.append(sticker)

        return stickers if is_list else stickers[0]
