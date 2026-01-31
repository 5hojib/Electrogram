# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class PrivacyRule(Enum):
    """Privacy rules together with privacy keys indicate what can or can't someone do and are specified by a PrivacyRule constructor, and its input counterpart InputPrivacyRule."""

    PRIVACY_VALUE_ALLOW_ALL = auto()
    PRIVACY_VALUE_ALLOW_BOTS = auto()
    PRIVACY_VALUE_ALLOW_CHAT_PARTICIPANTS = auto()
    PRIVACY_VALUE_ALLOW_CLOSE_FRIENDS = auto()
    PRIVACY_VALUE_ALLOW_CONTACTS = auto()
    PRIVACY_VALUE_ALLOW_PREMIUM = auto()
    PRIVACY_VALUE_ALLOW_USERS = auto()
    PRIVACY_VALUE_DISALLOW_ALL = auto()
    PRIVACY_VALUE_DISALLOW_BOTS = auto()
    PRIVACY_VALUE_DISALLOW_CHAT_PARTICIPANTS = auto()
    PRIVACY_VALUE_DISALLOW_CONTACTS = auto()
    PRIVACY_VALUE_DISALLOW_USERS = auto()
