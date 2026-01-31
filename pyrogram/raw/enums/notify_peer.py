# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class NotifyPeer(Enum):
    """Object defines the set of users and/or groups that generate notifications."""

    NOTIFY_BROADCASTS = auto()
    NOTIFY_CHATS = auto()
    NOTIFY_FORUM_TOPIC = auto()
    NOTIFY_PEER = auto()
    NOTIFY_USERS = auto()
