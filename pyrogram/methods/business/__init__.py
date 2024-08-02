from __future__ import annotations

from .create_invoice_link import CreateInvoiceLink
from .get_business_connection import GetBusinessConnection
from .get_stars_transactions import GetStarsTransactions
from .get_stars_transactions_by_id import GetStarsTransactionsById


class TelegramBusiness(
    CreateInvoiceLink,
    GetBusinessConnection,
    GetStarsTransactions,
    GetStarsTransactionsById,
):
    pass
