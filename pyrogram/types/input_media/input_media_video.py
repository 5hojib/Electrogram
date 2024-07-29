from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

from .input_media import InputMedia

if TYPE_CHECKING:
    from pyrogram import enums
    from pyrogram.types.messages_and_media import MessageEntity


class InputMediaVideo(InputMedia):
    """A video to be sent inside an album.
    It is intended to be used with :obj:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str`` | ``BinaryIO``):
            Video to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a video from the Internet.

        thumb (``str``):
            Thumbnail of the video sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        duration (``int``, *optional*):
            Video duration.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
    """

    def __init__(
        self,
        media: str | BinaryIO,
        thumb: str | None = None,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        supports_streaming: bool = True,
        has_spoiler: bool | None = None,
    ) -> None:
        super().__init__(media, caption, parse_mode, caption_entities)

        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming
        self.has_spoiler = has_spoiler
