from __future__ import annotations

from enum import auto

from .auto_name import AutoName


class StoryPrivacy(AutoName):
    """Story privacy type enumeration used in :obj:`~pyrogram.types.Story`."""

    PUBLIC = auto()
    "Public stories"

    CLOSE_FRIENDS = auto()
    "Close_Friends stories"

    CONTACTS = auto()
    "Contacts only stories"

    PRIVATE = auto()
    "Private stories"

    NO_CONTACTS = auto()
    "Hide stories from contacts"
