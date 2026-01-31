# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class Peer(Enum):
    """Chat partner or group."""

    PEER_CHANNEL = auto()
    PEER_CHAT = auto()
    PEER_USER = auto()
