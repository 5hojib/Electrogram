# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class RequestPeerType(Enum):
    """Filtering criteria to use for the peer selection list shown to the user."""

    REQUEST_PEER_TYPE_BROADCAST = auto()
    REQUEST_PEER_TYPE_CHAT = auto()
    REQUEST_PEER_TYPE_USER = auto()
