from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

from .reaction_type import ReactionType

if TYPE_CHECKING:
    from pyrogram import raw


class ReactionCount(Object):
    """Represents a reaction added to a message along with the number of times it was added.

    Parameters:

        type (:obj:`~pyrogram.types.ReactionType`):
            Reaction type.

        total_count (``int``):
            Total reaction count.

        chosen_order (``int``):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        type: ReactionType,
        total_count: int,
        chosen_order: int,
    ) -> None:
        super().__init__()
        self.type = type
        self.total_count = total_count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        update: raw.types.ReactionCount,
    ) -> ReactionCount | None:
        return ReactionCount(
            type=ReactionType._parse(update.reaction),
            total_count=update.count,
            chosen_order=update.chosen_order,
        )
