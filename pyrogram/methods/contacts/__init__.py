from __future__ import annotations

from .add_contact import AddContact
from .delete_contacts import DeleteContacts
from .get_contacts import GetContacts
from .get_contacts_count import GetContactsCount
from .import_contacts import ImportContacts
from .search_contacts import SearchContacts


class Contacts(
    GetContacts,
    DeleteContacts,
    ImportContacts,
    GetContactsCount,
    AddContact,
    SearchContacts,
):
    pass
