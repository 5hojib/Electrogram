# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class PasswordKdfAlgo(Enum):
    """Key derivation function to use when generating the password hash for SRP two-factor authorization"""

    PASSWORD_KDF_ALGO_SHA256_SHA256_PBKDF2_HMACSHA512ITER100000_SHA256_MOD_POW = auto()
    PASSWORD_KDF_ALGO_UNKNOWN = auto()
