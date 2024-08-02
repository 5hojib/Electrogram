from __future__ import annotations

from pyrogram.types.object import Object


class ForumTopicReopened(Object):
    """A service message about a forum topic reopened in the chat.

    Currently holds no information.
    """

    def __init__(self) -> None:
        super().__init__()
