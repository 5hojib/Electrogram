from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class InlineKeyboardMarkup(Object):
    """An inline keyboard that appears right next to the message it belongs to.

    Parameters:
        inline_keyboard (List of List of :obj:`~pyrogram.types.InlineKeyboardButton` | :obj:`~pyrogram.types.InlineKeyboardButtonBuy`):
            List of button rows, each represented by a List of InlineKeyboardButton objects.
            :obj:`~pyrogram.types.InlineKeyboardButtonBuy` objects is only for :meth:`~pyrogram.Client.send_invoice`.
            and only one needed in the first row.
    """

    def __init__(
        self,
        inline_keyboard: list[
            list[types.InlineKeyboardButton | types.InlineKeyboardButtonBuy]
        ],
    ) -> None:
        super().__init__()

        self.inline_keyboard = inline_keyboard

    @staticmethod
    def read(o):
        inline_keyboard = []

        for i in o.rows:
            row = [types.InlineKeyboardButton.read(j) for j in i.buttons]

            inline_keyboard.append(row)

        return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

    async def write(self, client: pyrogram.Client):
        rows = []

        for r in self.inline_keyboard:
            buttons = [await b.write(client) for b in r]

            rows.append(raw.types.KeyboardButtonRow(buttons=buttons))

        return raw.types.ReplyInlineMarkup(rows=rows)

        # There seems to be a Python issues with nested async comprehensions.
        # See: https://bugs.python.org/issue33346
        #
        # return raw.types.ReplyInlineMarkup(
        #     rows=[raw.types.KeyboardButtonRow(
        #         buttons=[await j.write(client) for j in i]
        #     ) for i in self.inline_keyboard]
        # )
