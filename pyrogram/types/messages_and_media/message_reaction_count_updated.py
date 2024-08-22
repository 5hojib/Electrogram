from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object
from pyrogram.types.update import Update

if TYPE_CHECKING:
    from datetime import datetime


class MessageReactionCountUpdated(Object, Update):
    """Reactions to a message with anonymous reactions were changed.

    These updates are heavy and their changes may be delayed by a few minutes.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            The chat containing the message the user reacted to

        message_id (``int``):
            Unique identifier of the message inside the chat

        date (:py:obj:`~datetime.datetime`):
            Date of change of the reaction

        reactions (:obj:`~pyrogram.types.ReactionCount`):
            List of reactions that are present on the message
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        chat: types.Chat,
        message_id: int,
        date: datetime,
        reactions: list[types.ReactionCount],
    ) -> None:
        super().__init__(client)

        self.chat = chat
        self.message_id = message_id
        self.date = date
        self.reactions = reactions

    @staticmethod
    def _parse(
        client: pyrogram.Client,
        update: raw.types.UpdateBotMessageReactions,
        users: dict[int, raw.types.User],
        chats: dict[int, raw.types.Chat],
    ) -> MessageReactionCountUpdated:
        chat = None
        peer_id = utils.get_peer_id(update.peer)
        raw_peer_id = utils.get_raw_peer_id(update.peer)
        if peer_id > 0:
            chat = types.Chat._parse_user_chat(client, users[raw_peer_id])
        else:
            chat = types.Chat._parse_chat_chat(client, chats[raw_peer_id])

        return MessageReactionCountUpdated(
            client=client,
            chat=chat,
            message_id=update.msg_id,
            date=utils.timestamp_to_datetime(update.date),
            reactions=[
                types.ReactionCount._parse(client, rt) for rt in update.reactions
            ],
        )
