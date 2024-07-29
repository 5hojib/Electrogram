from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import types


class PaymentInfo(Object):
    """Contains information about a payment.

    Parameters:
        name (``str``, *optional*):
            User's name.

        phone_number (``str``, *optional*):
            User's phone number.

        email (``str``, *optional*):
            User's email.

        shipping_address (:obj:`~pyrogram.types.ShippingAddress`, *optional*):
            User's shipping address.
    """

    def __init__(
        self,
        *,
        name: str | None = None,
        phone_number: str | None = None,
        email: str | None = None,
        shipping_address: types.ShippingAddress = None,
    ) -> None:
        super().__init__()

        self.name = name
        self.phone_number = phone_number
        self.email = email
        self.shipping_address = shipping_address
