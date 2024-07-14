import pyrogram
from pyrogram import raw
from typing import Union


class ReopenForumTopic:
    async def reopen_forum_topic(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        topic_id: int
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=topic_id,
                closed=False
            )
        )
        return True
