from datetime import datetime
from typing import Dict, List

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object
from ..update import Update


class MessageReactionCountUpdated(Object, Update):

    def __init__(
        self,
        *,
        client: pyrogram.Client | None = None,
        chat: types.Chat,
        message_id: int,
        date: datetime,
        reactions: List[types.ReactionCount]
    ):
        super().__init__(client)

        self.chat = chat
        self.message_id = message_id
        self.date = date
        self.reactions = reactions

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        update: raw.types.UpdateBotMessageReactions,
        users: Dict[int, raw.types.User],
        chats: Dict[int, raw.types.Chat]
    ) -> "MessageReactionCountUpdated":
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)

        chat = (
            types.Chat._parse_user_chat(client, users[raw_peer_id])
            if peer_id > 0
            else types.Chat._parse_chat_chat(client, chats[raw_peer_id])
        )

        return MessageReactionCountUpdated(
            client=client,
            chat=chat,
            message_id=update.msg_id,
            date=utils.timestamp_to_datetime(update.date),
            reactions=[types.ReactionCount._parse(rt) for rt in update.reactions]
        )