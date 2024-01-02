import pyrogram
from pyrogram import raw
from .menu_button import MenuButton


class MenuButtonDefault(MenuButton):
    def __init__(self):
        super().__init__("default")

    async def write(self, client: "pyrogram.Client") -> "raw.types.BotMenuButtonDefault":
        return raw.types.BotMenuButtonDefault()
