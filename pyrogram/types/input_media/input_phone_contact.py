from pyrogram import raw
from pyrogram.session.internals import MsgId
from ..object import Object


class InputPhoneContact(Object):
    def __init__(self, phone: str, first_name: str, last_name: str = ""):
        super().__init__(None)

    def __new__(cls, phone: str, first_name: str, last_name: str = ""):
        return raw.types.InputPhoneContact(
            client_id=MsgId(),
            phone="+" + phone.strip("+"),
            first_name=first_name,
            last_name=last_name,
        )
