from typing import Optional

import pyrogram
from pyrogram import types, enums


class EditInlineCaption:
    async def edit_inline_caption(
        self: "pyrogram.Client",
        inline_message_id: str,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
    ) -> bool:
        return await self.edit_inline_text(
            inline_message_id=inline_message_id,
            text=caption,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
        )
