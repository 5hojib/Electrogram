import os

import pyrogram
from pyrogram import raw
from pyrogram.utils import compute_password_hash, btoi, itob


class EnableCloudPassword:
    async def enable_cloud_password(
        self: "pyrogram.Client",
        password: str,
        hint: str = "",
        email: str = None
    ) -> bool:
        r = await self.invoke(raw.functions.account.GetPassword())

        if r.has_password:
            raise ValueError("There is already a cloud password enabled")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=raw.types.InputCheckPasswordEmpty(),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=hint,
                    email=email
                )
            )
        )

        return True
