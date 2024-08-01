from __future__ import annotations

import pyrogram
from pyrogram import raw


class HideGeneralTopic:
    async def hide_general_topic(self: pyrogram.Client, chat_id: int | str) -> bool:
        """hide a general forum topic.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            `bool`: On success, a True is returned.

        Example:
            .. code-block:: python

                await app.hide_general_topic(chat_id)
        """
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=1,
                hidden=True,
            )
        )
        return True
