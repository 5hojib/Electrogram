from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class PeerChannel(Object):
    """A PeerChannel.


    Parameters:
        channel_id (``Integer``):
            Id of the channel.
    """

    def __init__(self, *, channel_id: int) -> None:
        super().__init__()

        self.channel_id = channel_id

    @staticmethod
    def _parse(action: raw.types.PeerChannel) -> PeerChannel:
        return PeerChannel(channel_id=getattr(action, "channel_id", None))
