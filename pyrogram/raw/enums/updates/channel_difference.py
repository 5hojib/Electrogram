# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class ChannelDifference(Enum):
    """Contains the difference (new messages) between our local channel state and the remote state"""

    CHANNEL_DIFFERENCE = auto()
    CHANNEL_DIFFERENCE_EMPTY = auto()
    CHANNEL_DIFFERENCE_TOO_LONG = auto()
