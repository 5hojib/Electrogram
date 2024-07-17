import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from .inline_session import get_session


class EditInlineReplyMarkup:
    async def edit_inline_reply_markup(
        self: "pyrogram.Client",
        inline_message_id: str,
        reply_markup: "types.InlineKeyboardMarkup" = None,
    ) -> bool:
        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = await get_session(self, dc_id)

        return await session.invoke(
            raw.functions.messages.EditInlineBotMessage(
                id=unpacked,
                reply_markup=await reply_markup.write(self) if reply_markup else None,
            ),
            sleep_threshold=self.sleep_threshold,
        )
