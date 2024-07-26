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

from pyrogram import raw, types, utils
from ..object import Object
from typing import Union


class MessageStory(Object):
    """Contains information about a forwarded story.

    Parameters:
        from_user (:obj:`~pyrogram.types.User`, *optional*):
            Sender of the story.
        
        sender_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Sender of the story. If the story is from channel.

        story_id (``int``):
            Unique story identifier.
    """

    def __init__(
        self,
        *,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        story_id: int
    ):
        super().__init__()

        self.from_user = from_user
        self.sender_chat = sender_chat
        self.story_id = story_id

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        message_story: "raw.types.MessageMediaStory"
    ) -> Union["MessageStory", "types.Story"]:
        from_user = None
        sender_chat = None
        user_id = None
        chat_id = None
        if isinstance(message_story.peer, raw.types.PeerChannel):
            chat_id = utils.get_channel_id(message_story.peer.channel_id)
            chat = await client.invoke(
                raw.functions.channels.GetChannels(
                    id=[await client.resolve_peer(chat_id)]
                )
            )
            sender_chat = types.Chat._parse_chat(client, chat.chats[0])
        else:
            user_id = message_story.peer.user_id
            from_user = await client.get_users(user_id)
        if not client.me.is_bot:
            return await client.get_stories(user_id or chat_id, message_story.id)
        return MessageStory(
            from_user=from_user,
            sender_chat=sender_chat,
            story_id=message_story.id
        )
