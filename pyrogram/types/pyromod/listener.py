from asyncio import Future
from dataclasses import dataclass
from typing import Callable

import pyrogram

from .identifier import Identifier

@dataclass
class Listener:
    listener_type: pyrogram.enums.ListenerTypes
    filters: "pyrogram.filters.Filter"
    unallowed_click_alert: bool
    identifier: Identifier
    future: Future = None
    callback: Callable = None
