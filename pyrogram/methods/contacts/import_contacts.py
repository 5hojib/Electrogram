from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types


class ImportContacts:
    async def import_contacts(
        self: "pyrogram.Client",
        contacts: List["types.InputPhoneContact"]
    ):
        imported_contacts = await self.invoke(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts
