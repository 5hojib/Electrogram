#  Pyrofork - Telegram MTProto API Client Library for Python
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
import pyrogram
from pyrogram import raw
from pyrogram import types
from typing import Union


class EditForumTopic:
    async def edit_forum_topic(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        topic_id: int,
        title: str = None,
        icon_emoji_id: int = None
    ) -> bool:
        """Edit a forum topic.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                You can also use chat public link in form of *t.me/<username>* (str).

            topic_id (``int``):
                Unique identifier (int) of the target forum topic.

            title (``str``, *optional*):
                The forum topic title.

            icon_emoji_id (``int``, *optional*):
                Unique identifier of the custom emoji shown as the topic icon

        Returns:
            `bool`: On success, a Boolean is returned.

        Example:
            .. code-block:: python

                await app.edit_forum_topic(chat_id,topic_id,"New Topic Title")
        """
        await self.invoke(
            raw.functions.channels.EditForumTopic(
                channel=await self.resolve_peer(chat_id),
                topic_id=topic_id,
                title=title,
                icon_emoji_id=icon_emoji_id
            )
        )
        return True
