from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class LabeledPrice(Object):
    """This object represents a price for goods or services.

    Parameters:
        label (``str``):
            Portion label.

        amount (``int``):
            Price of the product in the smallest units of the currency (integer, not float/double).
            The minimum amuont for telegram stars is 1.
            The minimum amount for other currencies is US$1.
            you need to add 2 extra zeros to the amount (except stars), example 100 for 1 usd.
    """

    def __init__(self, label: str, amount: int) -> None:
        self.label = label
        self.amount = amount

    def write(self):
        return raw.types.LabeledPrice(label=self.label, amount=self.amount)
