from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import raw


class Contact(Object):
    """A phone contact.

    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        user_id (``int``, *optional*):
            Contact's user identifier in Telegram.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a vCard.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        phone_number: str,
        first_name: str,
        last_name: str | None = None,
        user_id: int | None = None,
        vcard: str | None = None,
    ) -> None:
        super().__init__(client)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        contact: raw.types.MessageMediaContact,
    ) -> Contact:
        return Contact(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name or None,
            vcard=contact.vcard or None,
            user_id=contact.user_id or None,
            client=client,
        )
