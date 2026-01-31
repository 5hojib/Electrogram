from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class GiftedPremium(Object):
    """Telegram Premium was gifted to the user

    Parameters:
        gifter_user_id (``int``):
            The identifier of a user that gifted Telegram Premium; 0 if the gift was anonymous

        currency (``str``):
            Currency for the paid amount

        amount (``int``):
            The paid amount, in the smallest units of the currency

        cryptocurrency (``str``):
            Cryptocurrency used to pay for the gift; may be empty if none

        cryptocurrency_amount (``int``):
            The paid amount, in the smallest units of the cryptocurrency; 0 if none

        month_count (``int``):
            Number of months the Telegram Premium subscription will be active
    """

    def __init__(
        self,
        *,
        gifter_user_id: int | None = None,
        currency: str | None = None,
        amount: int | None = None,
        cryptocurrency: str | None = None,
        cryptocurrency_amount: int | None = None,
        month_count: int | None = None,
    ) -> None:
        super().__init__()

        self.gifter_user_id = gifter_user_id
        self.currency = currency
        self.amount = amount
        self.cryptocurrency = cryptocurrency
        self.cryptocurrency_amount = cryptocurrency_amount
        self.month_count = month_count

    @staticmethod
    async def _parse(
        client,  # noqa: ARG004
        gifted_premium: raw.types.MessageActionGiftPremium,
        gifter_user_id: int,
    ) -> GiftedPremium:
        return GiftedPremium(
            gifter_user_id=gifter_user_id,
            currency=gifted_premium.currency,
            amount=gifted_premium.amount,
            cryptocurrency=getattr(gifted_premium, "crypto_currency", None),
            cryptocurrency_amount=getattr(gifted_premium, "crypto_amount", None),
            month_count=gifted_premium.months,
        )
