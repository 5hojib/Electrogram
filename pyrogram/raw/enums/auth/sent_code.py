# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class SentCode(Enum):
    """Contains info on a confirmation code message sent via SMS, phone call or Telegram."""

    SENT_CODE = auto()
    SENT_CODE_PAYMENT_REQUIRED = auto()
    SENT_CODE_SUCCESS = auto()
