from __future__ import annotations

import pyrogram
from pyrogram import raw
from pyrogram.types.object import Object


class InlineKeyboardButtonBuy(Object):
    """One button of the inline keyboard.
    For simple invoice buttons.

    Parameters:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.
    """

    def __init__(self, text: str) -> None:
        super().__init__()

        self.text = str(text)

    @staticmethod
    def read(b):
        return InlineKeyboardButtonBuy(text=b.text)

    async def write(self, _: pyrogram.Client):
        return raw.types.KeyboardButtonBuy(text=self.text)
