from typing import BinaryIO

from pyrogram.types.messages_and_media import MessageEntity
from pyrogram.types.object import Object


class InputMedia(Object):
    """Content of a media message to be sent.

    It should be one of:

    - :obj:`~pyrogram.types.InputMediaAnimation`
    - :obj:`~pyrogram.types.InputMediaDocument`
    - :obj:`~pyrogram.types.InputMediaAudio`
    - :obj:`~pyrogram.types.InputMediaPhoto`
    - :obj:`~pyrogram.types.InputMediaVideo`
    """

    def __init__(
        self,
        media: str | BinaryIO,
        caption: str = "",
        parse_mode: str | None = None,
        caption_entities: list[MessageEntity] | None = None,
    ):
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
