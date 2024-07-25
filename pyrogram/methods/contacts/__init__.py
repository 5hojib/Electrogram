from .add_contact import AddContact
from .delete_contacts import DeleteContacts
from .get_contacts import GetContacts
from .get_contacts_count import GetContactsCount
from .import_contacts import ImportContacts


class Contacts(
    GetContacts,
    DeleteContacts,
    ImportContacts,
    GetContactsCount,
    AddContact
):
    pass
