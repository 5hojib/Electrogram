# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class SendMessageAction(Enum):
    """User actions. Use this to provide users with detailed info about their chat partner's actions: typing or sending attachments of all kinds."""

    SEND_MESSAGE_CANCEL_ACTION = auto()
    SEND_MESSAGE_CHOOSE_CONTACT_ACTION = auto()
    SEND_MESSAGE_CHOOSE_STICKER_ACTION = auto()
    SEND_MESSAGE_EMOJI_INTERACTION = auto()
    SEND_MESSAGE_EMOJI_INTERACTION_SEEN = auto()
    SEND_MESSAGE_GAME_PLAY_ACTION = auto()
    SEND_MESSAGE_GEO_LOCATION_ACTION = auto()
    SEND_MESSAGE_HISTORY_IMPORT_ACTION = auto()
    SEND_MESSAGE_RECORD_AUDIO_ACTION = auto()
    SEND_MESSAGE_RECORD_ROUND_ACTION = auto()
    SEND_MESSAGE_RECORD_VIDEO_ACTION = auto()
    SEND_MESSAGE_TEXT_DRAFT_ACTION = auto()
    SEND_MESSAGE_TYPING_ACTION = auto()
    SEND_MESSAGE_UPLOAD_AUDIO_ACTION = auto()
    SEND_MESSAGE_UPLOAD_DOCUMENT_ACTION = auto()
    SEND_MESSAGE_UPLOAD_PHOTO_ACTION = auto()
    SEND_MESSAGE_UPLOAD_ROUND_ACTION = auto()
    SEND_MESSAGE_UPLOAD_VIDEO_ACTION = auto()
    SPEAKING_IN_GROUP_CALL_ACTION = auto()
