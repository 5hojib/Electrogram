from __future__ import annotations

from pyrogram import raw
from pyrogram.session.internals import MsgId
from pyrogram.types.object import Object


class InputPhoneContact(Object):
    """A Phone Contact to be added to your Telegram address book.

    Intended to be used with :meth:`~pyrogram.Client.add_contacts()`.

    Parameters:
        phone (``str``):
            Contact's phone number

        first_name (``str``):
            Contact's first name

        last_name (``str``, *optional*):
            Contact's last name
    """

    def __init__(self, phone: str, first_name: str, last_name: str = "") -> None:
        super().__init__()
        self.phone = phone
        self.first_name = first_name
        self.last_name = last_name

    def __new__(cls, phone: str, first_name: str, last_name: str = ""):
        return raw.types.InputPhoneContact(
            client_id=MsgId(),
            phone="+" + phone.strip("+"),
            first_name=first_name,
            last_name=last_name,
        )
