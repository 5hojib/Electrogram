from enum import auto
from .auto_name import AutoName


class ReactionType(AutoName):
    EMOJI = auto()
    CUSTOM_EMOJI = auto()
