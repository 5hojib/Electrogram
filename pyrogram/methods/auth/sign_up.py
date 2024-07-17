import logging

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class SignUp:
    async def sign_up(
        self: "pyrogram.Client",
        phone_number: str,
        phone_code_hash: str,
        first_name: str,
        last_name: str = "",
    ) -> "types.User":
        phone_number = phone_number.strip(" +")

        r = await self.invoke(
            raw.functions.auth.SignUp(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                phone_code_hash=phone_code_hash,
            )
        )

        await self.storage.user_id(r.user.id)
        await self.storage.is_bot(False)

        return types.User._parse(self, r.user)
