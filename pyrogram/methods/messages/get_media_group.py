import logging
from typing import Union, List

import pyrogram
from pyrogram import types

log = logging.getLogger(__name__)


class GetMediaGroup:
    async def get_media_group(
        self: "pyrogram.Client", chat_id: Union[int, str], message_id: int
    ) -> List["types.Message"]:
        if message_id <= 0:
            raise ValueError("Passed message_id is negative or equal to zero.")

        messages = await self.get_messages(
            chat_id=chat_id,
            message_ids=[msg_id for msg_id in range(message_id - 9, message_id + 10)],
            replies=0,
        )

        media_group_id = (
            messages[9].media_group_id
            if len(messages) == 19
            else messages[message_id - 1].media_group_id
        )

        if media_group_id is None:
            raise ValueError("The message doesn't belong to a media group")

        return types.List(
            msg for msg in messages if msg.media_group_id == media_group_id
        )
