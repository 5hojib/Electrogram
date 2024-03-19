from datetime import datetime
from typing import Dict, List

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from ..update import Update


class MessageReactionUpdated(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        from_user: "types.User",
        actor_chat: "types.Chat",
        date: datetime,
        chat: "types.Chat",
        old_reaction: List["types.ReactionType"],
        new_reaction: List["types.ReactionType"]
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.actor_chat = actor_chat
        self.date = date
        self.chat = chat
        self.old_reaction = old_reaction
        self.new_reaction = new_reaction

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: "raw.types.UpdateBotMessageReaction",
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "MessageReactionUpdated":
        chat = None
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)
        if peer_id > 0:
            chat = types.Chat._parse_user_chat(client, users[raw_peer_id])
        else:
            chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])

        from_user = None
        actor_chat = None

        raw_actor_peer_id = utils.get_raw_peer_id(update.actor)
        actor_peer_id = utils.get_peer_id(update.actor)

        if actor_peer_id > 0:
            from_user = types.User._parse(client, users[raw_actor_peer_id])
        else:
            actor_chat = types.Chat._parse_channel_chat(client, chats[raw_actor_peer_id])

        return MessageReactionUpdated(
            client=client,
            id=update.msg_id,
            from_user=from_user,
            date=utils.timestamp_to_datetime(update.date),
            chat=chat,
            actor_chat=actor_chat,
            old_reaction=[
                types.ReactionType._parse(
                    rt
                ) for rt in update.old_reactions
            ],
            new_reaction=[
                types.ReactionType._parse(
                    rt
                ) for rt in update.new_reactions
            ]
        )