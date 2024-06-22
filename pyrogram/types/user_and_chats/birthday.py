from typing import Optional, Union

from pyrogram import raw
from pyrogram import enums
from ..object import Object


class Birthday(Object):
    def __init__(
        self,
        *,
        day: int,
        month: int,
        year: int
    ):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(birthday: "raw.types.Birthday" = None) -> "Birthday":
        return Birthday(
            day=birthday.day,
            month=birthday.month,
            year=birthday.year
        )

    async def write(self) -> "raw.types.Birthday":
        return raw.types.Birthday(
            day=self.day,
            month=self.month,
            year=self.year
        )
