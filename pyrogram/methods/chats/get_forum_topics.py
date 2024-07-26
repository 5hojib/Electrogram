#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

import logging
from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)


class GetForumTopics:
    async def get_forum_topics(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0
    ) -> Optional[AsyncGenerator["types.ForumTopic", None]]:
        """Get one or more topic from a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            limit (``int``, *optional*):
                Limits the number of topics to be retrieved.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ForumTopic` objects is returned.

        Example:
            .. code-block:: python

                # get all forum topics
                async for topic in app.get_forum_topics(chat_id):
                    print(topic)

        Raises:
            ValueError: In case of invalid arguments.
        """

        peer = await self.resolve_peer(chat_id)

        rpc = raw.functions.channels.GetForumTopics(channel=peer, offset_date=0, offset_id=0, offset_topic=0, limit=limit)

        r = await self.invoke(rpc, sleep_threshold=-1)

        for _topic in r.topics:
            yield types.ForumTopic._parse(_topic)
