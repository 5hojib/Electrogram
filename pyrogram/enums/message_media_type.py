from enum import auto
from .auto_name import AutoName

class MessageMediaType(AutoName):
    AUDIO = auto()
    DOCUMENT = auto()
    PHOTO = auto()
    STICKER = auto()
    VIDEO = auto()
    ANIMATION = auto()
    VOICE = auto()
    VIDEO_NOTE = auto()
    CONTACT = auto()
    LOCATION = auto()
    VENUE = auto()
    POLL = auto()
    WEB_PAGE_PREVIEW = auto()
    DICE = auto()
    GAME = auto()
    GIVEAWAY = auto()
    GIVEAWAY_RESULT = auto()
    STORY = auto()
