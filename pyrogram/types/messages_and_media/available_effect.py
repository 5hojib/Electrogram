from typing import Optional

from pyrogram import raw, types
from ..object import Object


class AvailableEffect(Object):
    def __init__(
        self,
        *,
        id: int,
        emoji: str,
        effect_sticker_id: int,
        sticker: Optional["types.Sticker"] = None,
        is_premium: Optional[bool] = None,
        static_icon_id: Optional[int] = None,
        effect_animation_id: Optional[int] = None
    ):
        super().__init__()

        self.id = id
        self.emoji = emoji
        self.effect_sticker_id = effect_sticker_id
        self.sticker = sticker
        self.is_premium = is_premium
        self.static_icon_id = static_icon_id
        self.effect_animation_id = effect_animation_id

    @staticmethod
    async def _parse(client, effect: "raw.types.AvailableEffect", document: "raw.types.Document" = None) -> "AvailableEffect":
        sticker = None

        if document:
            attributes = {type(i): i for i in document.attributes}
            sticker = await types.Sticker._parse(client, document, attributes)

        return AvailableEffect(
            id=effect.id,
            emoji=effect.emoticon,
            effect_sticker_id=effect.effect_sticker_id,
            sticker=sticker,
            is_premium=getattr(effect, "premium_required", None),
            static_icon_id=getattr(effect, "static_icon_id", None),
            effect_animation_id=getattr(effect, "effect_animation_id", None)
        )
