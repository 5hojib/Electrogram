from datetime import datetime

from pyrogram import raw, utils
from ..object import Object


class VideoChatScheduled(Object):
    """A service message about a voice chat scheduled in the chat.

    Parameters:
        start_date (:py:obj:`~datetime.datetime`):
            Point in time when the voice chat is supposed to be started by a chat administrator.
    """

    def __init__(self, *, start_date: datetime):
        super().__init__()

        self.start_date = start_date

    @staticmethod
    def _parse(
        action: "raw.types.MessageActionGroupCallScheduled",
    ) -> "VideoChatScheduled":
        return VideoChatScheduled(
            start_date=utils.timestamp_to_datetime(action.schedule_date)
        )
