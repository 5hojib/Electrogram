# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class SecurePasswordKdfAlgo(Enum):
    """KDF algorithm to use for computing telegram passport hash"""

    SECURE_PASSWORD_KDF_ALGO_PBKDF2_HMACSHA512ITER100000 = auto()
    SECURE_PASSWORD_KDF_ALGO_SHA512 = auto()
    SECURE_PASSWORD_KDF_ALGO_UNKNOWN = auto()
