from enum import auto
from .auto_name import AutoName

class UserStatus(AutoName):
    ONLINE = auto()
    OFFLINE = auto()
    RECENTLY = auto()
    LAST_WEEK = auto()
    LAST_MONTH = auto()
    LONG_AGO = auto()
