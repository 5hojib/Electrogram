from enum import auto
from .auto_name import AutoName


class ClientPlatform(AutoName):
    ANDROID = auto()
    IOS = auto()
    WP = auto()
    BB = auto()
    DESKTOP = auto()
    WEB = auto()
    UBP = auto()
    OTHER = auto()
