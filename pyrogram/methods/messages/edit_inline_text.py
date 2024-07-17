from typing import Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from .inline_session import get_session


class EditInlineText:
    async def edit_inline_text(
        self: "pyrogram.Client",
        inline_message_id: str,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        disable_web_page_preview: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
    ) -> bool:
        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = await get_session(self, dc_id)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                no_webpage=disable_web_page_preview or None,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
                **await self.parser.parse(text, parse_mode),
            ),
            sleep_threshold=self.sleep_threshold,
        )
