from __future__ import annotations

from pyrogram.types.object import Object


class GeneralTopicHidden(Object):
    """A service message about a general topic hidden in the chat.

    Currently holds no information.
    """

    def __init__(self) -> None:
        super().__init__()
