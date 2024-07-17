from typing import Union

import pyrogram
from pyrogram import raw


class GetDiscussionRepliesCount:
    async def get_discussion_replies_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
    ) -> int:
        r = await self.invoke(
            raw.functions.messages.GetReplies(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                offset_id=0,
                offset_date=0,
                add_offset=0,
                limit=1,
                max_id=0,
                min_id=0,
                hash=0,
            )
        )

        return r.count
