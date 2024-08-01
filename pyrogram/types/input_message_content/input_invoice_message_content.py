from __future__ import annotations

import logging

import pyrogram
from pyrogram import raw, types

from .input_message_content import InputMessageContent

log = logging.getLogger(__name__)


class InputInvoiceMessageContent(InputMessageContent):
    """Content of an invoice message to be sent as the result of an inline query.

    Parameters:
        title (``str``):
            Product name, 1-32 characters.

        description (``str``):
            Product description, 1-255 characters

        payload (``str`` | ``bytes``):
            Bot-defined invoice payload, 1-128 bytes. This will not be displayed to the user, use for your internal processes.

        currency (``str``):
            Three-letter ISO 4217 currency code, see `more on currencies <https://core.telegram.org/bots/payments#supported-currencies>`_. Pass ``XTR`` for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        prices (List of :obj:`~pyrogram.types.LabeledPrice`):
            Price breakdown, a JSON-serialized list of components (e.g. product price, tax, discount, delivery cost, delivery tax, bonus, etc.). Must contain exactly one item for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        provider_token (``str``, *optional*):
            Payment provider token, obtained via `@BotFather <https://t.me/botfather>`_. Pass an empty string for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        max_tip_amount (``int``, *optional*):
            The maximum accepted amount for tips in the smallest units of the currency (integer, **not** float/double). For example, for a maximum tip of ``US$ 1.45`` pass ``max_tip_amount = 145``. See the exp parameter in `currencies.json <https://core.telegram.org/bots/payments/currencies.json>`_, it shows the number of digits past the decimal point for each currency (2 for the majority of currencies). Defaults to 0. Not supported for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        suggested_tip_amounts (List of ``int``, *optional*):
            An array of suggested amounts of tips in the smallest units of the currency (integer, **not** float/double). At most 4 suggested tip amounts can be specified. The suggested tip amounts must be positive, passed in a strictly increased order and must not exceed ``max_tip_amount``.

        provider_data (``str``, *optional*):
            JSON-serialized data about the invoice, which will be shared with the payment provider. A detailed description of required fields should be provided by the payment provider.

        photo_url (``str``, *optional*):
            URL of the product photo for the invoice. Can be a photo of the goods or a marketing image for a service. People like it better when they see what they are paying for.

        photo_size (``int``, *optional*):
            Photo size in bytes

        photo_width (``int``, *optional*):
            Photo width

        photo_height (``int``, *optional*):
            Photo height

        need_name (``bool``, *optional*):
            Pass True if you require the user's full name to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        need_phone_number (``bool``, *optional*):
            Pass True if you require the user's phone number to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        need_email (``bool``, *optional*):
            Pass True if you require the user's email address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        need_shipping_address (``bool``, *optional*):
            Pass True if you require the user's shipping address to complete the order. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        send_phone_number_to_provider (``bool``, *optional*):
            Pass True if the user's phone number should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        send_email_to_provider (``bool``, *optional*):
            Pass True if the user's email address should be sent to the provider. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

        is_flexible (``bool``, *optional*):
            Pass True if the final price depends on the shipping method. Ignored for payments in `Telegram Stars <https://t.me/BotNews/90>`_.

    """

    def __init__(
        self,
        title: str,
        description: str,
        payload: str | bytes,
        currency: str,
        prices: list[types.LabeledPrice],
        provider_token: str | None = None,
        max_tip_amount: int | None = None,
        suggested_tip_amounts: list[int] | None = None,
        provider_data: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_width: int | None = None,
        photo_height: int | None = None,
        need_name: bool | None = None,
        need_phone_number: bool | None = None,
        need_email: bool | None = None,
        need_shipping_address: bool | None = None,
        send_phone_number_to_provider: bool | None = None,
        send_email_to_provider: bool | None = None,
        is_flexible: bool | None = None,
    ) -> None:
        super().__init__()

        self.title = title
        self.description = description
        self.payload = payload
        self.currency = currency
        self.prices = prices
        self.provider_token = provider_token
        self.max_tip_amount = max_tip_amount
        self.suggested_tip_amounts = suggested_tip_amounts
        self.provider_data = provider_data
        self.photo_url = photo_url
        self.photo_size = photo_size
        self.photo_width = photo_width
        self.photo_height = photo_height
        self.need_name = need_name
        self.need_phone_number = need_phone_number
        self.need_email = need_email
        self.need_shipping_address = need_shipping_address
        self.send_phone_number_to_provider = send_phone_number_to_provider
        self.send_email_to_provider = send_email_to_provider
        self.is_flexible = is_flexible

    async def write(self, client: pyrogram.Client, reply_markup):
        return raw.types.InputBotInlineMessageMediaInvoice(
            title=self.title,
            description=self.description,
            photo=raw.types.InputWebDocument(
                url=self.photo_url,
                mime_type="image/jpg",
                size=self.photo_size,
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.photo_width, h=self.photo_height
                    )
                ],
            )
            if self.photo_url
            else None,
            invoice=raw.types.Invoice(
                currency=self.currency,
                prices=[i.write() for i in self.prices],
                test=client.test_mode,
                name_requested=self.need_name,
                phone_requested=self.need_phone_number,
                email_requested=self.need_email,
                shipping_address_requested=self.need_shipping_address,
                flexible=self.is_flexible,
                phone_to_provider=self.send_phone_number_to_provider,
                email_to_provider=self.send_email_to_provider,
            ),
            payload=self.payload.encode()
            if isinstance(self.payload, str)
            else self.payload,
            provider=self.provider_token,
            provider_data=raw.types.DataJSON(
                data=self.provider_data if self.provider_data else "{}"
            ),
            reply_markup=await reply_markup.write(client) if reply_markup else None,
        )
