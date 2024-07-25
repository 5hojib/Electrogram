from pyrogram import raw
from ..object import Object


class BusinessWeeklyOpen(Object):
    """Business weekly open hours.

    Parameters:
        start_minute (``int``):
            Start minute of the working day.

        end_minute (``int``):
            End minute of the working day.
    """

    def __init__(
        self,
        *,
        start_minute: int,
        end_minute: int,

    ):
        self.start_minute = start_minute
        self.end_minute = end_minute

    @staticmethod
    def _parse(weekly_open: "raw.types.BusinessWeeklyOpen" = None) -> "BusinessWeeklyOpen":
        return BusinessWeeklyOpen(
            start_minute=weekly_open.start_minute,
            end_minute=weekly_open.end_minute,
        )
