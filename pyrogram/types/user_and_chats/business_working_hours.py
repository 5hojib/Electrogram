from typing import Optional, List

from pyrogram import types, raw
from ..object import Object


class BusinessWorkingHours(Object):
    """Business working hours.

    Parameters:
        timezone (``str``):
            Timezone of the business.

        working_hours (List of :obj:`~pyrogram.types.BusinessWeeklyOpen`):
            Working hours of the business.

        is_open_now (``bool``, *optional*):
            True, if the business is open now.
    """

    def __init__(
        self,
        *,
        timezone: str,
        working_hours: List["types.BusinessWeeklyOpen"],
        is_open_now: bool = None

    ):
        self.timezone = timezone
        self.is_open_now = is_open_now
        self.working_hours = working_hours

    @staticmethod
    def _parse(work_hours: "raw.types.BusinessWorkHours" = None) -> Optional["BusinessWorkingHours"]:
        if not work_hours:
            return None

        return BusinessWorkingHours(
            timezone=work_hours.timezone_id,
            working_hours=types.List(
                types.BusinessWeeklyOpen._parse(i) for i in work_hours.weekly_open
            ),
            is_open_now=getattr(work_hours, "open_now", None),
        )
