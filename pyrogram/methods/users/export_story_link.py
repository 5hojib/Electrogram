from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

log = logging.getLogger(__name__)


class ExportStoryLink:
    async def export_story_link(
        self: pyrogram.Client,
        chat_id: int | str,
        story_id: int,
    ) -> types.ExportedStoryLink:
        """Get one story link from an user by using story identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user/channel.
                For your personal story you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use user profile/channel public link in form of *t.me/<username>* (str).

            story_id (``int``):
                Pass a single story identifier of story (as integers).

        Returns:
            :obj:`~pyrogram.types.ExportedStoryLink`: a single story link is returned.

        Example:
            .. code-block:: python

                # Get story link
                await app.export_story_link(chat_id, 12345)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.stories.ExportStoryLink(peer=peer, id=story_id)

        r = await self.invoke(rpc, sleep_threshold=-1)

        return types.ExportedStoryLink._parse(r)
