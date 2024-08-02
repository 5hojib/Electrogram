from __future__ import annotations

from pyrogram.types.object import Object


class GiveawayLaunched(Object):
    """A service message about a giveaway started in the channel.

    Currently holds no information.
    """

    def __init__(self) -> None:
        super().__init__()
