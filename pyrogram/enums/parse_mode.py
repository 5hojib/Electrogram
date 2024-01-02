from enum import auto
from .auto_name import AutoName

class ParseMode(AutoName):
    DEFAULT = auto()
    MARKDOWN = auto()
    HTML = auto()
    DISABLED = auto()
