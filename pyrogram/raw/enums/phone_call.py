# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class PhoneCall(Enum):
    """Phone call"""

    PHONE_CALL = auto()
    PHONE_CALL_ACCEPTED = auto()
    PHONE_CALL_DISCARDED = auto()
    PHONE_CALL_EMPTY = auto()
    PHONE_CALL_REQUESTED = auto()
    PHONE_CALL_WAITING = auto()
