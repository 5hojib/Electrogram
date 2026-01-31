# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class DocumentAttribute(Enum):
    """Various possible attributes of a document (used to define if it's a sticker, a GIF, a video, a mask sticker, an image, an audio, and so on)"""

    DOCUMENT_ATTRIBUTE_ANIMATED = auto()
    DOCUMENT_ATTRIBUTE_AUDIO = auto()
    DOCUMENT_ATTRIBUTE_CUSTOM_EMOJI = auto()
    DOCUMENT_ATTRIBUTE_FILENAME = auto()
    DOCUMENT_ATTRIBUTE_HAS_STICKERS = auto()
    DOCUMENT_ATTRIBUTE_IMAGE_SIZE = auto()
    DOCUMENT_ATTRIBUTE_STICKER = auto()
    DOCUMENT_ATTRIBUTE_VIDEO = auto()
