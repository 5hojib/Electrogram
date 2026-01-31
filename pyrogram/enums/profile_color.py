from __future__ import annotations

from .auto_name import AutoName


class ProfileColor(AutoName):
    """Profile color enumeration used in :meth:`~pyrogram.Client.update_color` and :obj:`~pyrogram.types.ChatColor`."""

    RED = 0
    "Red color."

    ORANGE = 1
    "Orange color."

    VIOLET = 2
    "Violet color."

    GREEN = 3
    "Green color."

    CYAN = 4
    "Cyan color."

    BLUE = 5
    "Blue color."

    PINK = 6
    "Pink color."

    GRAY = 7
    "Gray color."

    RED_LIGHT_RED = 8
    "Red color with light red gradient."

    ORANGE_LIGHT_ORANGE = 9
    "Orange color with light red gradient."

    VIOLET_LIGHT_VIOLET = 10
    "Violet color with light violet gradient."

    GREEN_LIGHT_GREEN = 11
    "Green color with light green gradien."

    CYAN_LIGHT_CYAN = 12
    "Cyan color with light cyan gradient."

    BLUE_LIGHT_BLUE = 13
    "Blue color with light blue gradient."

    PINK_LIGHT_PINK = 14
    "Pink color with light pink gradient."

    GRAY_LIGHT_GRAY = 15
    "Gray color with light gray gradient."
