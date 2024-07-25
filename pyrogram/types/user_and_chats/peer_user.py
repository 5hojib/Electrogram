from pyrogram import raw
from ..object import Object


class PeerUser(Object):
    """A PeerUser.


    Parameters:
        user_id (``Integer``):
            Id of the user.
    """

    def __init__(self, *, user_id: int):
        super().__init__()

        self.user_id = user_id

    @staticmethod
    def _parse(action: "raw.types.PeerUser") -> "PeerUser":
        return PeerUser(user_id=getattr(action, "user_id", None))
