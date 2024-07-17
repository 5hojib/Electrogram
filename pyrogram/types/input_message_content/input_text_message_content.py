from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils, enums
from .input_message_content import InputMessageContent


class InputTextMessageContent(InputMessageContent):
    def __init__(
        self,
        message_text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
    ):
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_web_page_preview = disable_web_page_preview

    async def write(self, client: "pyrogram.Client", reply_markup):
        message, entities = (
            await utils.parse_text_entities(
                client, self.message_text, self.parse_mode, self.entities
            )
        ).values()

        return raw.types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            message=message,
            entities=entities,
        )
