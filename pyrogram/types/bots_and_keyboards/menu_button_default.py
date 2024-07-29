from __future__ import annotations

import pyrogram
from pyrogram import raw

from .menu_button import MenuButton


class MenuButtonDefault(MenuButton):
    """Describes that no specific value for the menu button was set."""

    def __init__(self) -> None:
        super().__init__("default")

    async def write(
        self, client: pyrogram.Client
    ) -> raw.types.BotMenuButtonDefault:
        return raw.types.BotMenuButtonDefault()
