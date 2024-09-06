from __future__ import annotations

from pyrogram.types.object import Object


class ContactRegistered(Object):
    """A service message that a contact has registered with Telegram.
    Currently holds no information.
    """

    def __init__(self) -> None:
        super().__init__()
