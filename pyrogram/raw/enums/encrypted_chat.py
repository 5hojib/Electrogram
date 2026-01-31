# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class EncryptedChat(Enum):
    """Object contains info on an encrypted chat."""

    ENCRYPTED_CHAT = auto()
    ENCRYPTED_CHAT_DISCARDED = auto()
    ENCRYPTED_CHAT_EMPTY = auto()
    ENCRYPTED_CHAT_REQUESTED = auto()
    ENCRYPTED_CHAT_WAITING = auto()
