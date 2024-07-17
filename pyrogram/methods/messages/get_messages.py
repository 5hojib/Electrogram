import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)


class GetMessages:
    async def get_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1,
    ) -> Union["types.Message", List["types.Message"]]:
        ids, ids_type = (
            (message_ids, raw.types.InputMessageID)
            if message_ids
            else (reply_to_message_ids, raw.types.InputMessageReplyTo)
            if reply_to_message_ids
            else (None, None)
        )

        if ids is None:
            raise ValueError(
                "No argument supplied. Either pass message_ids or reply_to_message_ids"
            )

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [ids_type(id=i) for i in ids]

        if replies < 0:
            replies = (1 << 31) - 1

        if isinstance(peer, raw.types.InputPeerChannel):
            rpc = raw.functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = raw.functions.messages.GetMessages(id=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        messages = await utils.parse_messages(self, r, replies=replies)

        return messages if is_iterable else messages[0] if messages else None
