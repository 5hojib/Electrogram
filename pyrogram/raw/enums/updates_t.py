# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class Updates(Enum):
    """Object which is perceived by the client without a call on its part when an event occurs."""

    UPDATE_SHORT = auto()
    UPDATE_SHORT_CHAT_MESSAGE = auto()
    UPDATE_SHORT_MESSAGE = auto()
    UPDATE_SHORT_SENT_MESSAGE = auto()
    UPDATES = auto()
    UPDATES_COMBINED = auto()
    UPDATES_TOO_LONG = auto()
