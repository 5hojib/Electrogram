from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import types


class PaidMediaPreview(Object):
    """The paid media isn't available before the payment.
    Parameters:
        width (``int``, *optional*):
            Media width as defined by the sender.
        height (``int``, *optional*):
            Media height as defined by the sender.
        duration (``int``, *optional*):
            Duration of the media in seconds as defined by the sender.
        thumbnail (:obj:`~pyrogram.types.StrippedThumbnail`, *optional*):
            Media thumbnail.
    """

    def __init__(
        self,
        *,
        width: int | None = None,
        height: int | None = None,
        duration: int | None = None,
        thumbnail: types.StrippedThumbnail = None,
    ) -> None:
        super().__init__()

        self.width = width
        self.height = height
        self.duration = duration
        self.thumbnail = thumbnail
