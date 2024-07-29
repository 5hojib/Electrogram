from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import uuid4

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import types


class InlineQueryResult(Object):
    """One result of an inline query.

    - :obj:`~pyrogram.types.InlineQueryResultCachedAudio`
    - :obj:`~pyrogram.types.InlineQueryResultCachedDocument`
    - :obj:`~pyrogram.types.InlineQueryResultCachedAnimation`
    - :obj:`~pyrogram.types.InlineQueryResultCachedPhoto`
    - :obj:`~pyrogram.types.InlineQueryResultCachedSticker`
    - :obj:`~pyrogram.types.InlineQueryResultCachedVideo`
    - :obj:`~pyrogram.types.InlineQueryResultCachedVoice`
    - :obj:`~pyrogram.types.InlineQueryResultArticle`
    - :obj:`~pyrogram.types.InlineQueryResultAudio`
    - :obj:`~pyrogram.types.InlineQueryResultContact`
    - :obj:`~pyrogram.types.InlineQueryResultDocument`
    - :obj:`~pyrogram.types.InlineQueryResultAnimation`
    - :obj:`~pyrogram.types.InlineQueryResultLocation`
    - :obj:`~pyrogram.types.InlineQueryResultPhoto`
    - :obj:`~pyrogram.types.InlineQueryResultVenue`
    - :obj:`~pyrogram.types.InlineQueryResultVideo`
    - :obj:`~pyrogram.types.InlineQueryResultVoice`
    """

    def __init__(
        self,
        type: str,
        id: str,
        input_message_content: types.InputMessageContent,
        reply_markup: types.InlineKeyboardMarkup,
    ) -> None:
        super().__init__()

        self.type = type
        self.id = str(uuid4()) if id is None else str(id)
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup

    async def write(self, client: pyrogram.Client) -> None:
        pass
