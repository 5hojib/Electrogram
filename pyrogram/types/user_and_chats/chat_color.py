from typing import Optional, Union

from pyrogram import raw
from pyrogram import enums
from ..object import Object


class ChatColor(Object):
    def __init__(
        self,
        *,
        color: Union["enums.ReplyColor", "enums.ProfileColor"] = None,
        background_emoji_id: int = None
    ):
        self.color = color
        self.background_emoji_id = background_emoji_id

    @staticmethod
    def _parse(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ReplyColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )

    @staticmethod
    def _parse_profile_color(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ProfileColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )