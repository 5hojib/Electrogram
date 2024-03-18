from pyrogram import raw
from ..object import Object


class InputReplyToStory(Object):
    def __init__(
        self, *,
        peer: "raw.types.InputPeer" = None,
        story_id: int = None
    ):
        super().__init__()

        self.peer = peer
        self.story_id = story_id

    def write(self):
        return raw.types.InputReplyToStory(
            peer=self.peer,
            story_id=self.story_id
        ).write()
