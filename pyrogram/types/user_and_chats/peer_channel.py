from pyrogram import raw
from ..object import Object


class PeerChannel(Object):
    """A PeerChannel.


    Parameters:
        channel_id (``Integer``):
            Id of the channel.
    """

    def __init__(
        self, *,
        channel_id: int
    ):
        super().__init__()

        self.channel_id = channel_id

    @staticmethod
    def _parse(action: "raw.types.PeerChannel") -> "PeerChannel":


        return PeerChannel(
            channel_id=getattr(action,"channel_id", None)
        )
