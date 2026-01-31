from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import Iterable


class GetUsers:
    async def get_users(
        self: pyrogram.Client,
        user_ids: int | str | Iterable[int | str],
    ) -> types.User | list[types.User]:
        """Get information about a user.
        You can retrieve up to 200 users at once.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            user_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``):
                A list of User identifiers (id or username) or a single user id/username.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile link in form of *t.me/<username>* (str).

        Returns:
            :obj:`~pyrogram.types.User` | List of :obj:`~pyrogram.types.User`: In case *user_ids* was not a list,
            a single user is returned, otherwise a list of users is returned.

        Example:
            .. code-block:: python

                # Get information about one user
                await app.get_users("me")

                # Get information about multiple users at once
                await app.get_users([user_id1, user_id2, user_id3])
        """

        is_iterable = not isinstance(user_ids, int | str)
        user_ids = list(user_ids) if is_iterable else [user_ids]
        user_ids = await asyncio.gather(*[self.resolve_peer(i) for i in user_ids])

        r = await self.invoke(raw.functions.users.GetUsers(id=user_ids))

        users = types.List()

        for i in r:
            users.append(types.User._parse(self, i))

        return users if is_iterable else users[0]
