import pyrogram
from pyrogram import raw
from pyrogram.utils import compute_password_check


class RemoveCloudPassword:
    async def remove_cloud_password(self: "pyrogram.Client", password: str) -> bool:
        r = await self.invoke(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to remove")

        await self.invoke(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=raw.types.PasswordKdfAlgoUnknown(),
                    new_password_hash=b"",
                    hint="",
                ),
            )
        )

        return True
