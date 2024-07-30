from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class PeerUser(Object):
    """A PeerUser.


    Parameters:
        user_id (``Integer``):
            Id of the user.
    """

    def __init__(self, *, user_id: int) -> None:
        super().__init__()

        self.user_id = user_id

    @staticmethod
    def _parse(action: raw.types.PeerUser) -> PeerUser:
        return PeerUser(user_id=getattr(action, "user_id", None))
