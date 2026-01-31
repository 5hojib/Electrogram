# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class InputNotifyPeer(Enum):
    """Object defines the set of users and/or groups that generate notifications."""

    INPUT_NOTIFY_BROADCASTS = auto()
    INPUT_NOTIFY_CHATS = auto()
    INPUT_NOTIFY_FORUM_TOPIC = auto()
    INPUT_NOTIFY_PEER = auto()
    INPUT_NOTIFY_USERS = auto()
