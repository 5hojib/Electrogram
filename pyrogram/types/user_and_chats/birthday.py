from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class Birthday(Object):
    """User Date of birth.

    Parameters:
        day (``int``):
            Day of birth.

        month (``int``):
            Month of birth.

        year (``int``):
            Year of birth.
    """

    def __init__(self, *, day: int, month: int, year: int) -> None:
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(birthday: raw.types.Birthday = None) -> Birthday:
        return Birthday(day=birthday.day, month=birthday.month, year=birthday.year)

    async def write(self) -> raw.types.Birthday:
        return raw.types.Birthday(day=self.day, month=self.month, year=self.year)
