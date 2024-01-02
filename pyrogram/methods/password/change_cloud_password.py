import os

import pyrogram
from pyrogram import raw
from pyrogram.utils import compute_password_hash, compute_password_check, btoi, itob


class ChangeCloudPassword:
    async def change_cloud_password(
        self: "pyrogram.Client",
        current_password: str,
        new_password: str,
        new_hint: str = ""
    ) -> bool:
        r = await self.invoke(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to change")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, new_password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, current_password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=new_hint
                )
            )
        )

        return True
