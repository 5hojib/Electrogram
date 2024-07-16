import pyrogram
from pyrogram import raw
from typing import Union


class EditGeneralTopic:
    async def edit_general_topic(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        title: str
    ) -> bool:
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=1,
                title=title
            )
        )
        return True
