from __future__ import annotations

import logging
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types

if TYPE_CHECKING:
    from collections.abc import Iterable

log = logging.getLogger(__name__)


class GetForumTopicsByID:
    async def get_forum_topics_by_id(
        self: pyrogram.Client,
        chat_id: int | str,
        topic_ids: int | Iterable[int],
    ) -> types.ForumTopic | list[types.ForumTopic]:
        """Get one or more topic from a chat by using topic identifiers.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            topic_ids (``int`` | Iterable of ``int``, *optional*):
                Pass a single topic identifier or an iterable of topic ids (as integers) to get the information of the
                topic themselves.

        Returns:
            :obj:`~pyrogram.types.ForumTopic` | List of :obj:`~pyrogram.types.ForumTopic`: In case *topic_ids* was not
            a list, a single topic is returned, otherwise a list of topics is returned.

        Example:
            .. code-block:: python

                # Get one topic
                await app.get_forum_topics_by_id(chat_id, 12345)

                # Get more than one topic (list of topics)
                await app.get_forum_topics_by_id(chat_id, [12345, 12346])

        Raises:
            ValueError: In case of invalid arguments.
        """
        ids, _ids_type = (topic_ids, int) if topic_ids else (None, None)

        if ids is None:
            raise ValueError("No argument supplied. Either pass topic_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = list(ids)

        rpc = raw.functions.channels.GetForumTopicsByID(channel=peer, topics=ids)

        r = await self.invoke(rpc, sleep_threshold=-1)

        if is_iterable:
            topic_list = [types.ForumTopic._parse(topic) for topic in r.topics]
            topics = types.List(topic_list)
        else:
            topics = types.ForumTopic._parse(r.topics[0])

        return topics
