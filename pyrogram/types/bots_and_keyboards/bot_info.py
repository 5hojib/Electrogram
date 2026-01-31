from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class BotInfo(Object):
    """A bot Information.

    Parameters:
        name (``str``):
            The bot name.

        about (``str``):
            The bot bio.

        description (``str``):
            Description of the bot;
    """

    def __init__(self, name: str, about: str, description: str) -> None:
        super().__init__()

        self.name = name
        self.about = about
        self.description = description

    @staticmethod
    def _parse(bot_info: raw.types.bots.BotInfo) -> BotInfo:
        return BotInfo(
            name=getattr(bot_info, "name", None),
            about=getattr(bot_info, "about", None),
            description=getattr(bot_info, "description", None),
        )
