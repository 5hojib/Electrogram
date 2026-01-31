from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import raw, types


class PaymentRefunded(Object):
    """Contains information about a refunded payment.

    Parameters:
        user (:obj:`~pyrogram.types.User`):
            The user that refunded the payment.

        currency (``str``):
            Three-letter ISO 4217 currency code.

        total_amount (``int``):
            Total price in the smallest units of the currency.

        payload (``str``, *optional*):
            Bot specified invoice payload. Only available to the bot that received the payment.

        telegram_payment_charge_id (``str``, *optional*):
            Telegram payment identifier.

        provider_payment_charge_id (``str``, *optional*):
            Provider payment identifier.
    """

    def __init__(
        self,
        *,
        user: types.User,
        currency: str,
        total_amount: str,
        telegram_payment_charge_id: str,
        provider_payment_charge_id: str,
        payload: str | None = None,
    ) -> None:
        self.user = user
        self.currency = currency
        self.total_amount = total_amount
        self.telegram_payment_charge_id = telegram_payment_charge_id
        self.provider_payment_charge_id = provider_payment_charge_id
        self.payload = payload

    @staticmethod
    async def _parse(
        client: pyrogram.Client,
        payment_refunded: raw.types.MessageActionPaymentRefunded,
    ) -> PaymentRefunded:
        try:
            payload = payment_refunded.payload.decode()
        except (UnicodeDecodeError, AttributeError):
            payload = payment_refunded.payload

        return PaymentRefunded(
            user=await client.get_users(payment_refunded.peer.user_id),
            currency=payment_refunded.currency,
            total_amount=payment_refunded.total_amount,
            telegram_payment_charge_id=payment_refunded.charge.id
            if payment_refunded.charge.id != ""
            else None,
            provider_payment_charge_id=payment_refunded.charge.provider_charge_id
            if payment_refunded.charge.provider_charge_id != ""
            else None,
            payload=payload,
        )
