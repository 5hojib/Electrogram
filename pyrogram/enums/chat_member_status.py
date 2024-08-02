from __future__ import annotations

from enum import auto

from .auto_name import AutoName


class ChatMemberStatus(AutoName):
    """Chat member status enumeration used in :obj:`~pyrogram.types.ChatMember`."""

    OWNER = auto()
    "Chat owner"

    ADMINISTRATOR = auto()
    "Chat administrator"

    MEMBER = auto()
    "Chat member"

    RESTRICTED = auto()
    "Restricted chat member"

    LEFT = auto()
    "Left chat member"

    BANNED = auto()
    "Banned chat member"
