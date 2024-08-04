from __future__ import annotations

import pyrogram
from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeDefault(BotCommandScope):
    """Represents the default scope of bot commands.
    Default commands are used if no commands with a narrower scope are specified for the user.
    """

    def __init__(self) -> None:
        super().__init__("default")

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopeDefault()
