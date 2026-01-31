# # # # # # # # # # # # # # # # # # # # # # # #
#               !!! WARNING !!!               #
#          This is a generated file!          #
# All changes made in this file will be lost! #
# # # # # # # # # # # # # # # # # # # # # # # #

from enum import Enum, auto


class BotCommandScope(Enum):
    """Represents a scope where the bot commands, specified using bots.setBotCommands will be valid."""

    BOT_COMMAND_SCOPE_CHAT_ADMINS = auto()
    BOT_COMMAND_SCOPE_CHATS = auto()
    BOT_COMMAND_SCOPE_DEFAULT = auto()
    BOT_COMMAND_SCOPE_PEER = auto()
    BOT_COMMAND_SCOPE_PEER_ADMINS = auto()
    BOT_COMMAND_SCOPE_PEER_USER = auto()
    BOT_COMMAND_SCOPE_USERS = auto()
