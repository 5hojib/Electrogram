from __future__ import annotations

from .answer_pre_checkout_query import AnswerPreCheckoutQuery
from .answer_shipping_query import AnswerShippingQuery
from .create_invoice_link import CreateInvoiceLink
from .get_business_connection import GetBusinessConnection
from .get_stars_transactions import GetStarsTransactions
from .get_stars_transactions_by_id import GetStarsTransactionsById
from .refund_stars_payment import RefundStarPayment
from .send_invoice import SendInvoice
from .get_payment_form import GetPaymentForm
from .send_payment_form import SendPaymentForm
from .send_paid_media import SendPaidMedia


class TelegramBusiness(
    AnswerPreCheckoutQuery,
    AnswerShippingQuery,
    CreateInvoiceLink,
    GetBusinessConnection,
    GetStarsTransactions,
    GetStarsTransactionsById,
    RefundStarPayment,
    SendInvoice,
    SendPaidMedia,
    GetPaymentForm,
    SendPaymentForm,
):
    pass
