from .advanced import Advanced
from .auth import Auth
from .bots import Bots
from .chats import Chats
from .contacts import Contacts
from .decorators import Decorators
from .invite_links import InviteLinks
from .messages import Messages
from .password import Password
from .stickers import Stickers
from .users import Users
from .utilities import Utilities
from .business import TelegramBusiness


class Methods(
    Advanced,
    Auth,
    Bots,
    Contacts,
    Password,
    Chats,
    Stickers,
    Users,
    Messages,
    Decorators,
    Utilities,
    InviteLinks,
    TelegramBusiness,
):
    pass
