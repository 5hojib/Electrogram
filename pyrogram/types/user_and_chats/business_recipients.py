from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class BusinessRecipients(Object):
    """Business recipients.

    Parameters:
        existing_chats (``bool``, *optional*):
            True, if the message should be sent to existing chats.

        new_chats (``bool``, *optional*):
            True, if the message should be sent to new chats.

        contacts (``bool``, *optional*):
            True, if the message should be sent to contacts.

        non_contacts (``bool``, *optional*):
            True, if the message should be sent to non-contacts.

        exclude_selected (``bool``, *optional*):
            True, if the message should be sent to non-selected contacts.

        users (List of :obj:`~pyrogram.types.User`, *optional*):
            Recipients of the message.
    """

    def __init__(
        self,
        *,
        existing_chats: bool | None = None,
        new_chats: bool | None = None,
        contacts: bool | None = None,
        non_contacts: bool | None = None,
        exclude_selected: bool | None = None,
        users: list[int] | None = None,
    ) -> None:
        self.existing_chats = existing_chats
        self.new_chats = new_chats
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.exclude_selected = exclude_selected
        self.users = users

    @staticmethod
    def _parse(
        client,
        recipients: raw.types.BusinessRecipients,
        users: dict | None = None,
    ) -> BusinessRecipients:
        return BusinessRecipients(
            existing_chats=getattr(recipients, "existing_chats", None),
            new_chats=getattr(recipients, "new_chats", None),
            contacts=getattr(recipients, "contacts", None),
            non_contacts=getattr(recipients, "non_contacts", None),
            exclude_selected=getattr(recipients, "exclude_selected", None),
            users=types.List(
                types.User._parse(client, users[i]) for i in recipients.users
            )
            or None
            if getattr(recipients, "users", None)
            else None,
        )
