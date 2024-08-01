from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram


class InputMessageContent(Object):
    """Content of a message to be sent as a result of an inline query.

    Telegram clients currently support the following 5 types:

    - :obj:`~pyrogram.types.InputTextMessageContent`
    - :obj:`~pyrogram.types.InputLocationMessageContent`
    - :obj:`~pyrogram.types.InputVenueMessageContent`
    - :obj:`~pyrogram.types.InputContactMessageContent`
    - :obj:`~pyrogram.types.InputInvoiceMessageContent`

    """

    def __init__(self) -> None:
        super().__init__()

    async def write(self, client: pyrogram.Client, reply_markup) -> NoReturn:
        raise NotImplementedError
