from datetime import datetime
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw, utils
from pyrogram import types


class ForwardMessages:
    async def forward_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        message_thread_id: int = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        drop_author: bool = None
    ) -> Union["types.Message", List["types.Message"]]:
        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        r = await self.invoke(
            raw.functions.messages.ForwardMessages(
                to_peer=await self.resolve_peer(chat_id),
                from_peer=await self.resolve_peer(from_chat_id),
                id=message_ids,
                top_msg_id=message_thread_id,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids],
                schedule_date=utils.datetime_to_timestamp(schedule_date),
                noforwards=protect_content,
                drop_author=drop_author
            )
        )

        forwarded_messages = []

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage,
                              raw.types.UpdateNewScheduledMessage)):
                forwarded_messages.append(
                    await types.Message._parse(
                        self, i.message,
                        users, chats
                    )
                )

        return types.List(forwarded_messages) if is_iterable else forwarded_messages[0]
