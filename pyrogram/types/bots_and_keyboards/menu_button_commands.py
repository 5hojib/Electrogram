from __future__ import annotations

import pyrogram
from pyrogram import raw

from .menu_button import MenuButton


class MenuButtonCommands(MenuButton):
    """A menu button, which opens the bot's list of commands."""

    def __init__(self) -> None:
        super().__init__("commands")

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ) -> raw.types.BotMenuButtonCommands:
        return raw.types.BotMenuButtonCommands()
