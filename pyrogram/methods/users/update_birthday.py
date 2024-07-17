import pyrogram
from pyrogram import raw, types


class UpdateBirthday:
    async def update_birthday(
        self: "pyrogram.Client", day: int, month: int, year: int = None
    ) -> bool:
        birthday = types.Birthday(day=day, month=month, year=year)
        birthday = await birthday.write()

        r = await self.invoke(raw.functions.account.UpdateBirthday(birthday=birthday))
        if r:
            return True
        return False
