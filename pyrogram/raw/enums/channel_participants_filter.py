# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class ChannelParticipantsFilter(Enum):
    """Filter for fetching channel participants"""

    CHANNEL_PARTICIPANTS_ADMINS = auto()
    CHANNEL_PARTICIPANTS_BANNED = auto()
    CHANNEL_PARTICIPANTS_BOTS = auto()
    CHANNEL_PARTICIPANTS_CONTACTS = auto()
    CHANNEL_PARTICIPANTS_KICKED = auto()
    CHANNEL_PARTICIPANTS_MENTIONS = auto()
    CHANNEL_PARTICIPANTS_RECENT = auto()
    CHANNEL_PARTICIPANTS_SEARCH = auto()
