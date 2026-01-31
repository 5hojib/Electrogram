# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class SentCodeType(Enum):
    """Type of the verification code that was sent"""

    SENT_CODE_TYPE_APP = auto()
    SENT_CODE_TYPE_CALL = auto()
    SENT_CODE_TYPE_EMAIL_CODE = auto()
    SENT_CODE_TYPE_FIREBASE_SMS = auto()
    SENT_CODE_TYPE_FLASH_CALL = auto()
    SENT_CODE_TYPE_FRAGMENT_SMS = auto()
    SENT_CODE_TYPE_MISSED_CALL = auto()
    SENT_CODE_TYPE_SET_UP_EMAIL_REQUIRED = auto()
    SENT_CODE_TYPE_SMS = auto()
    SENT_CODE_TYPE_SMS_PHRASE = auto()
    SENT_CODE_TYPE_SMS_WORD = auto()
