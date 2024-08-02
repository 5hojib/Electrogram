from __future__ import annotations

from typing import TYPE_CHECKING

from .handler import Handler

if TYPE_CHECKING:
    from collections.abc import Callable


class ShippingQueryHandler(Handler):
    """The ShippingQueryHandler handler class. Used to handle shipping queries coming only from invoice buttons with flexible price.

    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_shipping_query` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new PreCheckoutQuery arrives. It takes *(client, shipping_query)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of callback queries to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        shipping_query (:obj:`~pyrogram.types.ShippingQuery`):
            New incoming shipping query. Only for invoices with flexible price.

    """

    def __init__(self, callback: Callable, filters=None) -> None:
        super().__init__(callback, filters)
