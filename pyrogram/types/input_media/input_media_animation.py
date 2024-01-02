from typing import Optional, List, Union, BinaryIO

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaAnimation(InputMedia):
    def __init__(
        self,
        media: Union[str, BinaryIO],
        thumb: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List[MessageEntity] = None,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        has_spoiler: bool = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.has_spoiler = has_spoiler
