from __future__ import annotations

import pyrogram
from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeAllPrivateChats(BotCommandScope):
    """Represents the scope of bot commands, covering all private chats."""

    def __init__(self) -> None:
        super().__init__("all_private_chats")

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopeUsers()
