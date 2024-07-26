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

from datetime import datetime
from pyrogram import raw, types, utils
from typing import Union
from ..object import Object
from ..update import Update

class StorySkipped(Object, Update):
    """A skipped story.

    Parameters:
        id (``int``):
            Unique story identifier.

        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.
        
        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story was sent.

        expire_date (:py:obj:`~datetime.datetime`, *optional*):
            Date the story will be expired.

        close_friends (``bool``, *optional*):
           True, if the Story is shared with close_friends only.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        date: datetime,
        expire_date: datetime,
        close_friends: bool = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.expire_date = expire_date
        self.close_friends = close_friends

    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"]
    ) -> "StorySkipped":
        from_user = None
        sender_chat = None
        if isinstance(peer, raw.types.PeerChannel):
            sender_chat = await client.get_chat(peer.channel_id)
        elif isinstance(peer, raw.types.InputPeerSelf):
            from_user = client.me
        else:
            from_user = await client.get_users(peer.user_id)

        return StorySkipped(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
            date=utils.timestamp_to_datetime(stories.date),
            expire_date=utils.timestamp_to_datetime(stories.expire_date),
            close_friends=stories.close_friends,
            client=client
        )
