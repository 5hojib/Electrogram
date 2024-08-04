from __future__ import annotations

import pyrogram
from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chat administrators."""

    def __init__(self) -> None:
        super().__init__("all_chat_administrators")

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopeChatAdmins()
