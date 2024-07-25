from typing import Optional

from pyrogram import raw
from .reaction_type import ReactionType
from ..object import Object

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
        chosen_order: int
    ):
        super().__init__()
        self.type = type
        self.total_count = total_count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        update: "raw.types.ReactionCount",
    ) -> Optional["ReactionCount"]:
        return ReactionCount(
            type=ReactionType._parse(
                update.reaction
            ),
            total_count=update.count,
            chosen_order=update.chosen_order
        )
