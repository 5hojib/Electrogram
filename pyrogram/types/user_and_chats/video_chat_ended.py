from pyrogram import raw
from ..object import Object


class VideoChatEnded(Object):
    """A service message about a voice chat ended in the chat.

    Parameters:
        duration (``int``):
            Voice chat duration; in seconds.
    """

    def __init__(self, *, duration: int):
        super().__init__()

        self.duration = duration

    @staticmethod
    def _parse(action: "raw.types.MessageActionGroupCall") -> "VideoChatEnded":
        return VideoChatEnded(duration=action.duration)
