from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

log = logging.getLogger(__name__)


class GetAllStories:
    async def get_all_stories(
        self: pyrogram.Client,
    ) -> AsyncGenerator[types.Story, None] | None:
        """Get all active stories.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.Story` objects is returned.

        Example:
            .. code-block:: python

                # Get all active story
                async for story in app.get_all_stories():
                    print(story)

        Raises:
            ValueError: In case of invalid arguments.
        """

        rpc = raw.functions.stories.GetAllStories()

        r = await self.invoke(rpc, sleep_threshold=-1)

        for peer_story in r.peer_stories:
            for story in peer_story.stories:
                yield await types.Story._parse(self, story, peer_story.peer)
