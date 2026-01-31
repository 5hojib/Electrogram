from __future__ import annotations

from pyrogram import enums, raw
from pyrogram.types.object import Object


class ChatColor(Object):
    """Reply or profile color status.

    Parameters:
        color (:obj:`~pyrogram.enums.ReplyColor` | :obj:`~pyrogram.enums.ProfileColor`, *optional*):
            Color type.

        background_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji.
    """

    def __init__(
        self,
        *,
        color: enums.ReplyColor | enums.ProfileColor = None,
        background_emoji_id: int | None = None,
    ) -> None:
        self.color = color
        self.background_emoji_id = background_emoji_id

    @staticmethod
    def _parse(
        color: raw.types.PeerColor = None,
    ) -> ChatColor | None:
        if not color:
            return None

        return ChatColor(
            color=enums.ReplyColor(color.color)
            if getattr(color, "color", None)
            else None,
            background_emoji_id=getattr(color, "background_emoji_id", None),
        )

    @staticmethod
    def _parse_profile_color(
        color: raw.types.PeerColor = None,
    ) -> ChatColor | None:
        if not color:
            return None

        return ChatColor(
            color=enums.ProfileColor(color.color)
            if getattr(color, "color", None)
            else None,
            background_emoji_id=getattr(color, "background_emoji_id", None),
        )
