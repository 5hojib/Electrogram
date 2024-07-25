from pyrogram import raw
from ..object import Object


class Username(Object):
    """A Username.


    Parameters:
        username (``String``):
            The channel/user username.

        editable (``bool``, *optional*):
            Can the username edited.

        active (``bool``, *optional*)
            Is the username active.
    """

    def __init__(
        self, *,
        username: str,
        editable: bool = None,
        active: bool = None
    ):
        super().__init__()

        self.username = username
        self.editable = editable
        self.active = active

    @staticmethod
    def _parse(action: "raw.types.Username") -> "Username":


        return Username(
            username=getattr(action,"username", None),
            editable=getattr(action,"editable", None),
            active=getattr(action,"active", None)
        )
