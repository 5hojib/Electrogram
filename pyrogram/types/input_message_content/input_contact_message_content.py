from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputContactMessageContent(InputMessageContent):
    """Content of a contact message to be sent as the result of an inline query.

    Parameters:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a `vCard <https://en.wikipedia.org/wiki/VCard>`_, 0-2048 bytes.

    """

    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str | None = None,
        vcard: str | None = None,
    ) -> None:
        super().__init__()

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard

    async def write(self, client: pyrogram.Client, reply_markup):
        return raw.types.InputBotInlineMessageMediaContact(
            phone_number=self.phone_number,
            first_name=self.first_name,
            last_name=self.last_name,
            vcard=self.vcard,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
