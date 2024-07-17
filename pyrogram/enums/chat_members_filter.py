from pyrogram import raw
from .auto_name import AutoName


class ChatMembersFilter(AutoName):
    SEARCH = raw.types.ChannelParticipantsSearch
    BANNED = raw.types.ChannelParticipantsKicked
    RESTRICTED = raw.types.ChannelParticipantsBanned
    BOTS = raw.types.ChannelParticipantsBots
    RECENT = raw.types.ChannelParticipantsRecent
    ADMINISTRATORS = raw.types.ChannelParticipantsAdmins
