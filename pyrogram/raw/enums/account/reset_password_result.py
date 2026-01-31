# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class ResetPasswordResult(Enum):
    """Result of an account.resetPassword request."""

    RESET_PASSWORD_FAILED_WAIT = auto()
    RESET_PASSWORD_OK = auto()
    RESET_PASSWORD_REQUESTED_WAIT = auto()
