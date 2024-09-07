from __future__ import annotations

from pyrogram.raw.core import Message, MsgContainer, TLObject
from pyrogram.raw.functions import Ping
from pyrogram.raw.types import HttpWait, MsgsAck

from .msg_id import MsgId
from .seq_no import SeqNo

not_content_related = (Ping, HttpWait, MsgsAck, MsgContainer)


class MsgFactory:
    def __init__(self) -> None:
        self.seq_no = SeqNo()

    def __call__(self, body: TLObject) -> Message:
        return Message(
            body,
            MsgId(),
            self.seq_no(not isinstance(body, not_content_related)),
            len(body),
        )
