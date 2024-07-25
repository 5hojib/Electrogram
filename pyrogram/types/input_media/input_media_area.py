from pyrogram import types

from ..object import Object


class InputMediaArea(Object):
    """Content of a media area to be included in story.

    Pyrofork currently supports the following types:

    - :obj:`~pyrogram.types.InputMediaAreaChannelPost`
    """

    # TODO: InputMediaAreaVenue

    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates"
    ):
        super().__init__()

        self.coordinates = coordinates
