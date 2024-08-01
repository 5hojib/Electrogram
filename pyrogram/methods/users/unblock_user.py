from __future__ import annotations

import pyrogram
from pyrogram import raw


class UnblockUser:
    async def unblock_user(self: pyrogram.Client, user_id: int | str) -> bool:
        """Unblock a user.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: True on success

        Example:
            .. code-block:: python

                await app.unblock_user(user_id)
        """
        return bool(
            await self.invoke(
                raw.functions.contacts.Unblock(id=await self.resolve_peer(user_id))
            )
        )
