from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class MessageInvoice(Object):
    """Contains information about an Invoice.

    Parameters:
        title (``str``):
            Product name.

        description (``str``):
            Product description.

        currency (``str``):
            Currency code.

        total_amount (``int``):
            Total price in the smallest units of the currency.

        start_parameter (``str``):
            Unique bot deep-linking parameter that can be used to generate this invoice.

        shipping_address_requested (``bool``, *optional*):
            True, if the the shipping address is requested.

        test (``bool``, *optional*):
            True, if the invoice is a test invoice.

        receipt_message_id (``int``, *optional*):
            The message_id of the message sent to the chat when the invoice is paid.
    """

    def __init__(
        self,
        *,
        title: str,
        description: str,
        currency: str,
        total_amount: int,
        start_parameter: str,
        shipping_address_requested: bool | None = None,
        test: bool | None = None,
        receipt_message_id: int | None = None,
        # TODO: Implement photo, extended_media parameters
    ) -> None:
        super().__init__()

        self.title = title
        self.description = description
        self.currency = currency
        self.total_amount = total_amount
        self.start_parameter = start_parameter
        self.shipping_address_requested = shipping_address_requested
        self.test = test
        self.receipt_message_id = receipt_message_id

    @staticmethod
    def _parse(
        message_invoice: "raw.types.MessageMediaInvoice",
    ) -> "MessageInvoice":
        return MessageInvoice(
            title=message_invoice.title,
            description=message_invoice.description,
            currency=message_invoice.currency,
            total_amount=message_invoice.total_amount,
            start_parameter=message_invoice.start_param,
            shipping_address_requested=message_invoice.shipping_address_requested,
            test=message_invoice.test,
            receipt_message_id=message_invoice.receipt_msg_id,
        )
