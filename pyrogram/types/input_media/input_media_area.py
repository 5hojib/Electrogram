from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import types


class InputMediaArea(Object):
    """Content of a media area to be included in story.

    Electrogram currently supports the following types:

    - :obj:`~pyrogram.types.InputMediaAreaChannelPost`
    """

    # TODO: InputMediaAreaVenue

    def __init__(self, coordinates: types.MediaAreaCoordinates) -> None:
        super().__init__()

        self.coordinates = coordinates
