from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class ChatAdminWithInviteLinks(Object):
    """Represents a chat administrator that has created invite links in a chat.

    Parameters:
        admin (:obj:`~pyrogram.types.User`):
            The administrator.

        chat_invite_links_count (``int``):
            The number of valid chat invite links created by this administrator.

        revoked_chat_invite_links_count (``int``):
            The number of revoked chat invite links created by this administrator.
    """

    def __init__(
        self,
        *,
        admin: types.User,
        chat_invite_links_count: int,
        revoked_chat_invite_links_count: int | None = None,
    ) -> None:
        super().__init__()

        self.admin = admin
        self.chat_invite_links_count = chat_invite_links_count
        self.revoked_chat_invite_links_count = revoked_chat_invite_links_count

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        admin: raw.types.ChatAdminWithInvites,
        users: dict[int, raw.types.User] | None = None,
    ) -> ChatAdminWithInviteLinks:
        return ChatAdminWithInviteLinks(
            admin=types.User._parse(client, users[admin.admin_id]),
            chat_invite_links_count=admin.invites_count,
            revoked_chat_invite_links_count=admin.revoked_invites_count,
        )
