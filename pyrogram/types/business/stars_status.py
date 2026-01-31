from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class StarsStatus(Object):
    """Contains information about stars status.

    Parameters:
        balance (``int``):
            Current balance of stars.

        history (List of :obj:`~pyrogram.types.StarsTransaction`):
            Stars transactions history.
    """

    def __init__(self, *, balance: int, history: list) -> None:
        super().__init__()

        self.balance = balance
        self.history = history

    @staticmethod
    def _parse(client, stars_status: raw.types.StarsStatus) -> StarsStatus:
        users = {user.id: user for user in stars_status.users}
        return StarsStatus(
            balance=stars_status.balance,
            history=[
                types.StarsTransaction._parse(client, history, users)
                for history in stars_status.history
            ],
        )
