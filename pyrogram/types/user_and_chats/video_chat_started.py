from __future__ import annotations

from pyrogram.types.object import Object


class VideoChatStarted(Object):
    """A service message about a voice chat started in the chat.

    Currently holds no information.
    """

    def __init__(self) -> None:
        super().__init__()
