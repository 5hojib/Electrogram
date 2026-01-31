# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class EmailVerification(Enum):
    """Email verification code or token"""

    EMAIL_VERIFICATION_APPLE = auto()
    EMAIL_VERIFICATION_CODE = auto()
    EMAIL_VERIFICATION_GOOGLE = auto()
