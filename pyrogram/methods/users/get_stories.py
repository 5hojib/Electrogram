import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)

class GetStories:
    async def get_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ) -> Union["types.Story", List["types.Story"]]:
        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]

        rpc = raw.functions.stories.GetStoriesByID(peer=peer, id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            return types.List([await types.Story._parse(self, story, peer) for story in r.stories])
        return await types.Story._parse(self, r.stories[0], peer)
