from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class VideoChatMembersInvited(Object):
    """A service message about new members invited to a voice chat.


    Parameters:
        users (List of :obj:`~pyrogram.types.User`):
            New members that were invited to the voice chat.
    """

    def __init__(self, *, users: list[types.User]) -> None:
        super().__init__()

        self.users = users

    @staticmethod
    def _parse(
        client,
        action: raw.types.MessageActionInviteToGroupCall,
        users: dict[int, raw.types.User],
    ) -> VideoChatMembersInvited:
        users = [types.User._parse(client, users[i]) for i in action.users]

        return VideoChatMembersInvited(users=users)
