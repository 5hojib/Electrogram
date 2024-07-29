from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram.types.messages_and_media import MessageEntity


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
    ) -> None:
        super().__init__()

        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
