from typing import Optional, List, Union, BinaryIO

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaPhoto(InputMedia):
    def __init__(
        self,
        media: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List[MessageEntity] = None,
        has_spoiler: bool = None
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.has_spoiler = has_spoiler
