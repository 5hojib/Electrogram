from pyrogram import raw
from ..object import Object
from typing import Union


class InputReplyToMessage(Object):
    def __init__(
        self, *,
        reply_to_message_id: int = None,
        message_thread_id: int = None,
        reply_to_chat: Union[
            "raw.types.InputPeerChannel",
            "raw.types.InputPeerUser"
        ] = None,
        quote_text: str = None
    ):
        super().__init__()

        self.reply_to_message_id = reply_to_message_id
        self.message_thread_id = message_thread_id
        self.reply_to_chat = reply_to_chat
        self.quote_text = quote_text

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
                quote_text=self.quote_text
            ).write()
        return None
