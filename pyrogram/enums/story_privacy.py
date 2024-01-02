from enum import auto
from .auto_name import AutoName

class StoryPrivacy(AutoName):
    PUBLIC = auto()
    CLOSE_FRIENDS = auto()
    CONTACTS = auto()
    PRIVATE = auto()
    NO_CONTACTS = auto()
