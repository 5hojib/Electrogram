from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types


class ImportContacts:
    async def import_contacts(
        self: "pyrogram.Client",
        contacts: List["types.InputPhoneContact"]
    ):
        """Import contacts to your Telegram address book.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            contacts (List of :obj:`~pyrogram.types.InputPhoneContact`):
                The contact list to be added

        Returns:
            :obj:`types.contacts.ImportedContacts`

        Example:
            .. code-block:: python

                from pyrogram.types import InputPhoneContact

                await app.import_contacts([
                    InputPhoneContact("+1-123-456-7890", "Foo"),
                    InputPhoneContact("+1-456-789-0123", "Bar"),
                    InputPhoneContact("+1-789-012-3456", "Baz")])
        """
        imported_contacts = await self.invoke(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
