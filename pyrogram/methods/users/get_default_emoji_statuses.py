from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class GetDefaultEmojiStatuses:
    async def get_default_emoji_statuses(
        self: pyrogram.Client,
    ) -> list[types.EmojiStatus]:
        """Get the default emoji statuses.

        .. include:: /_includes/usable-by/users-bots.rst

        Returns:
            List of :obj:`~pyrogram.types.EmojiStatus`: On success, a list of emoji statuses is returned.

        Example:
            .. code-block:: python

                default_emoji_statuses = await app.get_default_emoji_statuses()
                print(default_emoji_statuses)
        """
        r = await self.invoke(raw.functions.account.GetDefaultEmojiStatuses(hash=0))

        return types.List([types.EmojiStatus._parse(self, i) for i in r.statuses])
