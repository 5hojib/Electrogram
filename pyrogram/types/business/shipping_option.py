from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class ShippingOption(Object):
    """This object represents one shipping option.

    Parameters:
        id (``str``):
            Shipping option identifier.

        title (``str``):
            Option title.

        prices (List of :obj:`~pyrogram.types.LabeledPrice`):
            List of price portions.

    """

    def __init__(self, id: str, title: str, prices: types.LabeledPrice) -> None:
        super().__init__()

        self.id = id
        self.title = title
        self.prices = prices

    @staticmethod
    def _parse(
        shipping_option: raw.types.ShippingOption,
    ) -> ShippingOption:
        if isinstance(shipping_option, raw.types.ShippingOption):
            return ShippingOption(
                id=shipping_option.id,
                title=shipping_option.title,
                prices=[
                    types.LabeledPrice._parse(price)
                    for price in shipping_option.prices
                ],
            )
        return None

    def write(self):
        return raw.types.ShippingOption(
            id=self.id,
            title=self.title,
            prices=[price.write() for price in self.prices],
        )
