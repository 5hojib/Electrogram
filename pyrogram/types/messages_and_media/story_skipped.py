from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object
from pyrogram.types.update import Update

if TYPE_CHECKING:
    from datetime import datetime


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
        client: pyrogram.Client = None,
        id: int,
        from_user: types.User = None,
        sender_chat: types.Chat = None,
        date: datetime,
        expire_date: datetime,
        close_friends: bool | None = None,
    ) -> None:
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.expire_date = expire_date
        self.close_friends = close_friends

    async def _parse(
        self: pyrogram.Client,
        stories: raw.base.StoryItem,
        peer: raw.types.PeerChannel | raw.types.PeerUser,
    ) -> StorySkipped:
        from_user = None
        sender_chat = None
        if isinstance(peer, raw.types.PeerChannel):
            sender_chat = await self.get_chat(peer.channel_id)
        elif isinstance(peer, raw.types.InputPeerSelf):
            from_user = self.me
        else:
            from_user = await self.get_users(peer.user_id)

        return StorySkipped(
            id=stories.id,
            from_user=from_user,
            sender_chat=sender_chat,
            date=utils.timestamp_to_datetime(stories.date),
            expire_date=utils.timestamp_to_datetime(stories.expire_date),
            close_friends=stories.close_friends,
            client=self,
        )
