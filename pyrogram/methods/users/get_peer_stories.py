import logging
from typing import AsyncGenerator, Union, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)

class GetPeerStories:
    async def get_peer_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> Optional[AsyncGenerator["types.Story", None]]:
        peer = await self.resolve_peer(chat_id)


        rpc = raw.functions.stories.GetPeerStories(peer=peer)

        r = await self.invoke(rpc, sleep_threshold=-1)

        for story in r.stories.stories:
            yield await types.Story._parse(self, story, peer)
