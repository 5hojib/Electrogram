import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)

class DeleteStories:
    async def delete_stories(
        self: "pyrogram.Client",
        story_ids: Union[int, Iterable[int]],
        chat_id: int = None
    ) -> bool:
        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]
        
        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        try:
            await self.invoke(
                raw.functions.stories.DeleteStories(peer=peer,id=ids)
            )
        except Exception as e:
            print(e)
            return False
        return True
