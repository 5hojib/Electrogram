from __future__ import annotations

from .account import Account
from .advanced import Advanced
from .auth import Auth
from .bots import Bots
from .business import TelegramBusiness
from .chats import Chats
from .contacts import Contacts
from .decorators import Decorators
from .invite_links import InviteLinks
from .messages import Messages
from .password import Password
from .stickers import Stickers
from .users import Users
from .utilities import Utilities


class Methods(
    Account,
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
