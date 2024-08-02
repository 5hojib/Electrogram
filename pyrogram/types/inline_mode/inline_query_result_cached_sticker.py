from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.file_id import FileId

from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedSticker(InlineQueryResult):
    """A link to a sticker stored on the Telegram servers

    By default, this sticker will be sent by the user. Alternatively, you can use *input_message_content* to send a
    message with the specified content instead of the sticker.

    Parameters:
        sticker_file_id (``str``):
            A valid file identifier of the sticker.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the photo.
    """

    def __init__(
        self,
        sticker_file_id: str,
        id: str | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
        input_message_content: types.InputMessageContent = None,
    ) -> None:
        super().__init__("sticker", id, input_message_content, reply_markup)

        self.sticker_file_id = sticker_file_id
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self, client: pyrogram.Client):
        file_id = FileId.decode(self.sticker_file_id)

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            document=raw.types.InputDocument(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
            ),
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                    message="",
                )
            ),
        )
