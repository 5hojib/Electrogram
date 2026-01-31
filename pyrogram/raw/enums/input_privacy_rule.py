# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class InputPrivacyRule(Enum):
    """Privacy rules indicate who can or can't do something and are specified by a PrivacyRule, and its input counterpart InputPrivacyRule."""

    INPUT_PRIVACY_VALUE_ALLOW_ALL = auto()
    INPUT_PRIVACY_VALUE_ALLOW_BOTS = auto()
    INPUT_PRIVACY_VALUE_ALLOW_CHAT_PARTICIPANTS = auto()
    INPUT_PRIVACY_VALUE_ALLOW_CLOSE_FRIENDS = auto()
    INPUT_PRIVACY_VALUE_ALLOW_CONTACTS = auto()
    INPUT_PRIVACY_VALUE_ALLOW_PREMIUM = auto()
    INPUT_PRIVACY_VALUE_ALLOW_USERS = auto()
    INPUT_PRIVACY_VALUE_DISALLOW_ALL = auto()
    INPUT_PRIVACY_VALUE_DISALLOW_BOTS = auto()
    INPUT_PRIVACY_VALUE_DISALLOW_CHAT_PARTICIPANTS = auto()
    INPUT_PRIVACY_VALUE_DISALLOW_CONTACTS = auto()
    INPUT_PRIVACY_VALUE_DISALLOW_USERS = auto()
