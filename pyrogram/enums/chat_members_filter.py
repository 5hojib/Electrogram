from __future__ import annotations

from pyrogram import raw

from .auto_name import AutoName


class ChatMembersFilter(AutoName):
    """Chat members filter enumeration used in :meth:`~pyrogram.Client.get_chat_members`"""

    SEARCH = raw.types.ChannelParticipantsSearch
    "Search for members"

    BANNED = raw.types.ChannelParticipantsKicked
    "Banned members"

    RESTRICTED = raw.types.ChannelParticipantsBanned
    "Restricted members"

    BOTS = raw.types.ChannelParticipantsBots
    "Bots"

    RECENT = raw.types.ChannelParticipantsRecent
    "Recently active members"

    ADMINISTRATORS = raw.types.ChannelParticipantsAdmins
    "Administrators"
