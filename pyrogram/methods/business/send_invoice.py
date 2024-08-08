from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils


class SendInvoice:
    async def send_invoice(
        self: pyrogram.Client,
        chat_id: int | str,
        title: str,
        description: str,
        currency: str,
        prices: types.LabeledPrice | list[types.LabeledPrice],
        provider: str | None = None,
        provider_data: str | None = None,
        payload: str | None = None,
        photo_url: str | None = None,
        photo_size: int | None = None,
        photo_mime_type: str | None = None,
        start_parameter: str | None = None,
        extended_media: types.InputMedia = None,
        reply_to_message_id: int | None = None,
        message_thread_id: int | None = None,
        quote_text: str | None = None,
        quote_entities: list[types.MessageEntity] | None = None,
        reply_markup: types.InlineKeyboardMarkup = None,
    ):
        """Use this method to send invoices.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target private chat or username of the target private chat.

            title (``str``):
                Product name.

            description (``str``):
                Product description.

            currency (``str``):
                Three-letter ISO 4217 currency code.
                `XTR` for Telegram Stars.

            prices (:obj:`~pyrogram.types.LabeledPrice` | List of :obj:`~pyrogram.types.LabeledPrice`):
                Price with label.
                If you add multiple prices, the prices will be added up.
                For stars invoice you can only have one item.

            provider (``str``, *optional*):
                Payment provider.
                Get this from botfather.

            provider_data (``str``, *optional*):
                Provider data in json format.

            payload (``str``, *optional*):
                Bot-defined invoice payload, 1-128 bytes.
                This will not be displayed to the user, use for your internal processes.

            photo_url (``str``, *optional*):
                Photo URL.

            photo_size (``int``, *optional*):
                Photo size.

            photo_mime_type (``str``, *optional*):
                Photo MIME type.

            start_parameter (``str``, *optional*):
                Unique bot deep-linking parameter that can be used to generate this invoice.

            extended_media (:obj:`~pyrogram.types.InputMedia`, *optional*):
                Additional media.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            quote_text (``str``, *optional*):
                Text to quote.
                for reply_to_message only.

            quote_entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
                List of special entities that appear in quote_text, which can be specified instead of *parse_mode*.
                for reply_to_message only.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An inline keyboard. If empty, one 'Buy' button will be shown.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent message is returned.

        Example:
            .. code-block:: python

                # USD (single prices)
                app.send_invoice(
                    chat_id,
                    title="Product Name",
                    description="Product Description",
                    currency="USD",
                    prices=types.LabeledPrice("Product", 1000),
                    provider="Stripe_provider_codes",
                    provider_data="{}"
                )

                # USD (multiple prices)
                app.send_invoice(
                    chat_id,
                    title="Product Name",
                    description="Product Description",
                    currency="USD",
                    prices=[
                        types.LabeledPrice("Product 1", 1000),
                        types.LabeledPrice("Product 2", 2000)
                    ],
                    provider="Stripe_provider_codes",
                    provider_data="{}"
                )

                # Telegram Stars
                app.send_invoice(
                    chat_id,
                    title="Product Name",
                    description="Product Description",
                    currency="XTR",
                    prices=types.LabeledPrice("Product", 1000)
                )
        """

        is_iterable = not isinstance(prices, types.LabeledPrice)

        if reply_markup is not None:
            has_buy_button = False
            for i in reply_markup.inline_keyboard:
                for j in i:
                    if isinstance(j, types.InlineKeyboardButtonBuy):
                        has_buy_button = True
            if not has_buy_button:
                text = "Pay"
                if currency == "XTR":
                    prices_total = 0
                    for price in prices:
                        prices_total += price.amount
                    text = f"Pay ⭐️{prices_total}"
                reply_markup.inline_keyboard.insert(
                    0, [types.InlineKeyboardButtonBuy(text=text)]
                )

        reply_to = await utils.get_reply_to(
            client=self,
            chat_id=chat_id,
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
        )

        if payload is not None:
            encoded_payload = payload.encode()
        else:
            encoded_payload = f"{(title)}".encode()
        r = await self.invoke(
            raw.functions.messages.SendMedia(
                peer=await self.resolve_peer(chat_id),
                media=raw.types.InputMediaInvoice(
                    title=title,
                    description=description,
                    invoice=raw.types.Invoice(
                        currency=currency,
                        prices=[price.write() for price in prices]
                        if is_iterable
                        else [prices.write()],
                    ),
                    payload=encoded_payload,
                    provider=provider,
                    provider_data=raw.types.DataJSON(
                        data=provider_data if provider_data else "{}"
                    ),
                    photo=raw.types.InputWebDocument(
                        url=photo_url,
                        size=photo_size or 0,
                        mime_type=photo_mime_type or "image/jpeg",
                        attributes=[],
                    )
                    if photo_url
                    else None,
                    start_param=start_parameter,
                    extended_media=extended_media,
                ),
                random_id=self.rnd_id(),
                reply_to=reply_to,
                message="",
                reply_markup=await reply_markup.write(self)
                if reply_markup is not None
                else None,
            )
        )

        for i in r.updates:
            if isinstance(
                i, raw.types.UpdateNewMessage | raw.types.UpdateNewChannelMessage
            ):
                return await types.Message._parse(
                    self,
                    i.message,
                    users={i.id: i for i in r.users},
                    chats={i.id: i for i in r.chats},
                )
        return None
