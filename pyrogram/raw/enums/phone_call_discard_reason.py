# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class PhoneCallDiscardReason(Enum):
    """Why was the phone call discarded?"""

    PHONE_CALL_DISCARD_REASON_BUSY = auto()
    PHONE_CALL_DISCARD_REASON_DISCONNECT = auto()
    PHONE_CALL_DISCARD_REASON_HANGUP = auto()
    PHONE_CALL_DISCARD_REASON_MIGRATE_CONFERENCE_CALL = auto()
    PHONE_CALL_DISCARD_REASON_MISSED = auto()
