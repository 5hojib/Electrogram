from typing import Optional

from pyrogram import raw
from .reaction_type import ReactionType
from ..object import Object

class ReactionCount(Object):
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
