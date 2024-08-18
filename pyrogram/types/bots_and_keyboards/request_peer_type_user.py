from __future__ import annotations

from pyrogram.types.object import Object


class RequestPeerTypeUser(Object):
    """Object used to request clients to send a user identifier.

    Parameters:
        button_id (``int``, *optional*):
            Button identifier.

        is_bot (``bool``, *optional*):
            If True, show only Bots.

        is_premium (``bool``, *optional*):
            If True, show only Premium Users.

        max (``int``, *optional*):
            Maximum number of users to be returned.
            default 1.

        is_name_requested (``bool``, *optional*):
            If True, User name is requested.
            default True.

        is_username_requested (``bool``, *optional*):
            If True, User username is requested.
            default True.

        is_photo_requested (``bool``, *optional*):
            If True, User photo is requested.
            default True.
    """

    def __init__(
        self,
        button_id: int = 0,
        is_bot: bool | None = None,
        is_premium: bool | None = None,
        max: int = 1,
        is_name_requested: bool = True,
        is_username_requested: bool = True,
        is_photo_requested: bool = True,
    ) -> None:
        super().__init__()
        self.button_id = button_id
        self.is_bot = is_bot
        self.is_premium = is_premium
        self.max = max
        self.is_name_requested = is_name_requested
        self.is_username_requested = is_username_requested
        self.is_photo_requested = is_photo_requested
