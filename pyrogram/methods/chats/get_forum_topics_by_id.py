import logging
from typing import Union, List, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetForumTopicsByID:
    async def get_forum_topics_by_id(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        topic_ids: Union[int, Iterable[int]],
    ) -> Union["types.ForumTopic", List["types.ForumTopic"]]:
        ids, ids_type = (topic_ids, int) if topic_ids else (None, None)

        if ids is None:
            raise ValueError("No argument supplied. Either pass topic_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [i for i in ids]

        rpc = raw.functions.channels.GetForumTopicsByID(channel=peer, topics=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            topic_list = []
            for topic in r.topics:
                topic_list.append(types.ForumTopic._parse(topic))
            topics = types.List(topic_list)
        else:
            topics = types.ForumTopic._parse(r.topics[0])

        return topics
