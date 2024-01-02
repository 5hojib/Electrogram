from enum import auto
from .auto_name import AutoName

class ListenerTypes(AutoName):
    MESSAGE = auto()
    CALLBACK_QUERY = auto()
