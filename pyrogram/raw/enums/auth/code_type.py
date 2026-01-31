# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class CodeType(Enum):
    """Type of verification code that will be sent next if you call the resendCode method"""

    CODE_TYPE_CALL = auto()
    CODE_TYPE_FLASH_CALL = auto()
    CODE_TYPE_FRAGMENT_SMS = auto()
    CODE_TYPE_MISSED_CALL = auto()
    CODE_TYPE_SMS = auto()
