from __future__ import annotations

import pyrogram
from pyrogram import enums, raw, types, utils

from .input_message_content import InputMessageContent


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters:
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        disable_web_page_preview (``bool``, *optional*):
            Disables link previews for links in this message.
    """

    def __init__(
        self,
        message_text: str,
        parse_mode: enums.ParseMode | None = None,
        entities: list[types.MessageEntity] | None = None,
        disable_web_page_preview: bool | None = None,
    ) -> None:
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_web_page_preview = disable_web_page_preview

    async def write(self, client: pyrogram.Client, reply_markup):
        message, entities = (
            await utils.parse_text_entities(
                client,
                self.message_text,
                self.parse_mode,
                self.entities,
            )
        ).values()

        return raw.types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            message=message,
            entities=entities,
        )
