from __future__ import annotations

from pyrogram import raw

from .auto_name import AutoName


class BusinessSchedule(AutoName):
    """Business away enumeration used in :obj:`~pyrogram.types.BusinessInfo`."""

    ALWAYS = raw.types.BusinessAwayMessageScheduleAlways
    "Send always"

    OUTSIDE_WORK_HOURS = raw.types.BusinessAwayMessageScheduleOutsideWorkHours
    "Outside of Business Hours"

    CUSTOM = raw.types.BusinessAwayMessageScheduleCustom
    "Custom Schedule"
