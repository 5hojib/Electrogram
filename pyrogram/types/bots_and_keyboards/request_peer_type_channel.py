from __future__ import annotations

from pyrogram.types.object import Object


class RequestPeerTypeChannel(Object):
    """Object used to request clients to send a channel identifier.

    Parameters:
        button_id (``int``, *optional*):
            Button identifier.

        is_creator (``bool``, *optional*):
            If True, show only Channel which user is the owner.

        is_username (``bool``, *optional*):
            If True, show only Channel which has username.

        max (``int``, *optional*):
            Maximum number of channels to be returned.
            default 1.

        is_name_requested (``bool``, *optional*):
            If True, Channel name is requested.
            default True.

        is_username_requested (``bool``, *optional*):
            If True, Channel username is requested.
            default True.

        is_photo_requested (``bool``, *optional*):
            If True, Channel photo is requested.
            default True.
    """

    def __init__(
        self,
        button_id: int = 0,
        is_creator: bool | None = None,
        is_username: bool | None = None,
        max: int = 1,
        is_name_requested: bool = True,
        is_username_requested: bool = True,
        is_photo_requested: bool = True,
    ) -> None:
        super().__init__()

        self.button_id = button_id
        self.is_creator = is_creator
        self.is_username = is_username
        self.max = max
        self.is_name_requested = is_name_requested
        self.is_username_requested = is_username_requested
        self.is_photo_requested = is_photo_requested
