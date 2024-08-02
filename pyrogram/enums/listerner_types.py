from __future__ import annotations

from enum import auto

from .auto_name import AutoName


class ListenerTypes(AutoName):
    """Listener type enumeration used in :obj:`~pyrogram.types.Client`."""

    MESSAGE = auto()
    "A Message"

    CALLBACK_QUERY = auto()
    "A CallbackQuery"
