from typing import Optional, List, BinaryIO, Union

from .input_media import InputMedia
from ..messages_and_media import MessageEntity
from ... import enums


class InputMediaAudio(InputMedia):
    def __init__(
        self,
        media: Union[str, BinaryIO],
        thumb: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List[MessageEntity] = None,
        duration: int = 0,
        performer: str = "",
        title: str = ""
    ):
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title
