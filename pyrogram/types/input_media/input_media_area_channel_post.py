from __future__ import annotations

import pyrogram
from pyrogram import raw, types

from .input_media_area import InputMediaArea


class InputMediaAreaChannelPost(InputMediaArea):
    """A channel post media area.

    Parameters:
        coordinates (:obj:`~pyrogram.types.MediaAreaCoordinates`):
            Media area coordinates.

        chat_id (``int`` | ``str``):
            Unique identifier (int) or username (str) of the target channel.

        message_id (``int``):
            A single message id.
    """

    def __init__(
        self,
        coordinates: types.MediaAreaCoordinates,
        chat_id: int | str,
        message_id: int,
    ) -> None:
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat_id = chat_id
        self.message_id = message_id

    async def write(self, client: pyrogram.Client):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=self.coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id,
        )
