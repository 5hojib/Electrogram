from typing import Optional, List, Union, BinaryIO

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaDocument(InputMedia):
    def __init__(
        self,
        media: Union[str, BinaryIO],
        thumb: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List[MessageEntity] = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
