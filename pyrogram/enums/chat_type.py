from enum import auto
from .auto_name import AutoName

class ChatType(AutoName):
    PRIVATE = auto()
    BOT = auto()
    GROUP = auto()
    SUPERGROUP = auto()
    CHANNEL = auto()
