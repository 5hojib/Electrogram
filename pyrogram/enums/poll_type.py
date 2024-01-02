from enum import auto
from .auto_name import AutoName

class PollType(AutoName):
    QUIZ = auto()
    REGULAR = auto()
