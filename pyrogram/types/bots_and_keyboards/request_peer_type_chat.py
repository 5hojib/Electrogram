from __future__ import annotations

from pyrogram.types.object import Object


class RequestPeerTypeChat(Object):
    """Object used to request clients to send a chat identifier.

    Parameters:
        button_id (``int``, *optional*):
            Button identifier.

        is_creator (``bool``, *optional*):
            If True, show only Chat which user is the owner.

        is_bot_participant (``bool``, *optional*):
            If True, show only Chat where bot is a participant.

        is_username (``bool``, *optional*):
            If True, show only Chat which has username.

        is_forum (``bool``, *optional*):
            If True, show only Chat which is a forum.

        max (``int``, *optional*):
            Maximum number of chats to be returned.
            default 1.

        is_name_requested (``bool``, *optional*):
            If True, Chat name is requested.
            default True.

        is_username_requested (``bool``, *optional*):
            If True, Chat username is requested.
            default True.

        is_photo_requested (``bool``, *optional*):
            If True, Chat photo is requested.
            default True.
    """  # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        button_id: int = 0,
        is_creator: bool | None = None,
        is_bot_participant: bool | None = None,
        is_username: bool | None = None,
        is_forum: bool | None = None,
        max: int = 1,
        is_name_requested: bool = True,
        is_username_requested: bool = True,
        is_photo_requested: bool = True,
    ) -> None:
        super().__init__()

        self.button_id = button_id
        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.is_username = is_username
        self.is_forum = is_forum
        self.max = max
        self.is_name_requested = is_name_requested
        self.is_username_requested = is_username_requested
        self.is_photo_requested = is_photo_requested
