from __future__ import annotations

from enum import auto

from .auto_name import AutoName


class ChatJoinType(AutoName):
    """How the service message :obj:`~pyrogram.enums.MessageServiceType.NEW_CHAT_MEMBERS` was used for the member to join the chat."""

    BY_ADD = auto()
    "A new member joined the chat via an invite link"

    BY_LINK = auto()
    "A new member joined the chat via an invite link"

    BY_REQUEST = auto()
    "A new member was accepted to the chat by an administrator"
