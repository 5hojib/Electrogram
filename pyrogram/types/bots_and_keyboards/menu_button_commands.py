from __future__ import annotations

from pyrogram import raw

from .menu_button import MenuButton


class MenuButtonCommands(MenuButton):
    """A menu button, which opens the bot's list of commands."""

    def __init__(self) -> None:
        super().__init__("commands")

    async def write(self) -> raw.types.BotMenuButtonCommands:
        return raw.types.BotMenuButtonCommands()
