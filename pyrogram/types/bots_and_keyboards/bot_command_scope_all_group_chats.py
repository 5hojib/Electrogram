from __future__ import annotations

from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeAllGroupChats(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chats."""

    def __init__(self) -> None:
        super().__init__("all_group_chats")

    async def write(self) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopeChats()
