from __future__ import annotations

from pyrogram import raw
from pyrogram.types.object import Object


class InputStarsTransaction(Object):
    """Content of a stars transaction.

    Parameters:
        id (``str``):
            Unique transaction identifier.

        is_refund (``bool``, *optional*):
            True, if the transaction is a refund.
    """

    def __init__(self, *, id: str, is_refund: bool | None = None) -> None:
        super().__init__()

        self.id = id
        self.is_refund = is_refund

    async def write(self):
        return raw.types.InputStarsTransaction(id=self.id, refund=self.is_refund)
