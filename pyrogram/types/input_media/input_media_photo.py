from __future__ import annotations

from typing import TYPE_CHECKING, BinaryIO

from .input_media import InputMedia

if TYPE_CHECKING:
    from pyrogram import enums
    from pyrogram.types.messages_and_media import MessageEntity


class InputMediaPhoto(InputMedia):
    """A photo to be sent inside an album.
    It is intended to be used with :obj:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str`` | ``BinaryIO``):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine or
            pass a binary file-like object with its attribute “.name” set for in-memory uploads or
            pass an HTTP URL as a string for Telegram to get a photo from the Internet.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.
            If not specified, the original caption is kept. Pass "" (empty string) to remove the caption.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        has_spoiler (``bool``, *optional*):
            Pass True if the photo needs to be covered with a spoiler animation.
    """

    def __init__(
        self,
        media: str | BinaryIO,
        caption: str = "",
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[MessageEntity] | None = None,
        has_spoiler: bool | None = None,
    ) -> None:
        super().__init__(media, caption, parse_mode, caption_entities)

        self.has_spoiler = has_spoiler
