from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class InputReplyToMessage(Object):
    """Contains information about a target replied message.


    Parameters:
        reply_to_message_id (``int``, *optional*):
            ID of the original message you want to reply.

        message_thread_id (``int``, *optional*):
            Unique identifier for the target message thread (topic) of the forum.
            for forum supergroups only.

        reply_to_chat (:obj:`~pyrogram.raw.InputPeer`, *optional*):
            Unique identifier for the origin chat.
            for reply to message from another chat.

        quote_text (``str``, *optional*):
            Text to quote.
            for reply_to_message only.

        quote_entities (List of :obj:`~pyrogram.raw.base.MessageEntity`):
            Entities to quote.
            for reply_to_message only.
    """

    def __init__(
        self,
        *,
        reply_to_message_id: int | None = None,
        message_thread_id: int | None = None,
        reply_to_chat: raw.types.InputPeerChannel | raw.types.InputPeerUser = None,
        quote_text: str | None = None,
        quote_entities: list[raw.base.MessageEntity] | None = None,
    ) -> None:
        super().__init__()

        self.reply_to_message_id = reply_to_message_id
        self.message_thread_id = message_thread_id
        self.reply_to_chat = reply_to_chat
        self.quote_text = quote_text
        self.quote_entities = quote_entities

    def write(self):
        reply_to_msg_id = None
        top_msg_id = None
        if self.reply_to_message_id or self.message_thread_id:
            if self.message_thread_id:
                if not self.reply_to_message_id:
                    reply_to_msg_id = self.message_thread_id
                else:
                    reply_to_msg_id = self.reply_to_message_id
                top_msg_id = self.message_thread_id
            else:
                reply_to_msg_id = self.reply_to_message_id
            return raw.types.InputReplyToMessage(
                reply_to_msg_id=reply_to_msg_id,
                top_msg_id=top_msg_id,
                reply_to_peer_id=self.reply_to_chat,
                quote_text=self.quote_text,
                quote_entities=self.quote_entities,
            ).write()
        return None
