from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class VideoChatEnded(Object):
    """A service message about a voice chat ended in the chat.

    Parameters:
        duration (``int``):
            Voice chat duration; in seconds.
    """

    def __init__(self, *, duration: int) -> None:
        super().__init__()

        self.duration = duration

    @staticmethod
    def _parse(
        action: raw.types.MessageActionGroupCall,
    ) -> VideoChatEnded:
        return VideoChatEnded(duration=action.duration)
