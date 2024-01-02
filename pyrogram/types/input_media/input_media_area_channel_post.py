import pyrogram

from pyrogram import raw, types

from .input_media_area import InputMediaArea

from typing import Union

class InputMediaAreaChannelPost(InputMediaArea):
    def __init__(
        self,
        coordinates: "types.MediaAreaCoordinates",
        chat_id: Union[int, str],
        message_id: int
    ):
        super().__init__(coordinates=coordinates)

        self.coordinates = coordinates
        self.chat_id = chat_id
        self.message_id = message_id

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputMediaAreaChannelPost(
            coordinates=self.coordinates,
            channel=await client.resolve_peer(self.chat_id),
            msg_id=self.message_id
        )
