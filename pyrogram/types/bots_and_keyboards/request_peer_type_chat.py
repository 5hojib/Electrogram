from __future__ import annotations

from pyrogram.types.object import Object


class RequestPeerTypeChat(Object):
    """Object used to request clients to send a chat identifier.

    Parameters:
        is_creator (``bool``, *optional*):
            If True, show only Chat which user is the owner.

        is_bot_participant (``bool``, *optional*):
            If True, show only Chat where bot is a participant.

        is_username (``bool``, *optional*):
            If True, show only Chat which has username.

        is_forum (``bool``, *optional*):
            If True, show only Chat which is a forum.
    """  # TODO user_admin_rights, bot_admin_rights

    def __init__(
        self,
        is_creator: bool | None = None,
        is_bot_participant: bool | None = None,
        is_username: bool | None = None,
        is_forum: bool | None = None,
        max: int = 1,
    ) -> None:
        super().__init__()

        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.is_username = is_username
        self.is_forum = is_forum
        self.max = max
