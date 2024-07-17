from typing import Optional

from pyrogram import enums, raw
from ..object import Object


class ReactionType(Object):
    def __init__(
        self,
        *,
        type: str = "enums.ReactionType",
        emoji: str = None,
        custom_emoji_id: str = None,
    ):
        super().__init__()
        self.type = type
        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id

    @staticmethod
    def _parse(
        update: "raw.types.Reaction",
    ) -> Optional["ReactionType"]:
        if isinstance(update, raw.types.ReactionEmpty):
            return None
        elif isinstance(update, raw.types.ReactionEmoji):
            return ReactionType(type=enums.ReactionType.EMOJI, emoji=update.emoticon)
        elif isinstance(update, raw.types.ReactionCustomEmoji):
            return ReactionType(
                type=enums.ReactionType.CUSTOM_EMOJI, custom_emoji_id=update.document_id
            )

    def write(self):
        if self.type == enums.ReactionType.EMOJI:
            return raw.types.ReactionEmoji(emoticon=self.emoji)
        if self.type == enums.ReactionType.CUSTOM_EMOJI:
            return raw.types.ReactionCustomEmoji(document_id=self.custom_emoji_id)
