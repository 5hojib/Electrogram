from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class AvailableEffect(Object):
    """Contains information about available effect.

    Parameters:
        id (``int``):
            Unique effect identifier.

        emoji (``str``):
            Emoji that represents the effect.

        effect_sticker_id (``int``):
            sticker identifier that represents the effect.

        sticker (:obj:`~pyrogram.types.Sticker`, *optional*):
            Sticker that represents the effect.

        is_premium (``bool``, *optional*):
            Whether the effect is available only for premium users.

        static_icon_id (``int``, *optional*):
            Static icon identifier that represents the effect.

        effect_animation_id (``int``, *optional*):
            Animation identifier that represents the effect.
    """

    def __init__(
        self,
        *,
        id: int,
        emoji: str,
        effect_sticker_id: int,
        sticker: types.Sticker | None = None,
        is_premium: bool | None = None,
        static_icon_id: int | None = None,
        effect_animation_id: int | None = None,
    ) -> None:
        super().__init__()

        self.id = id
        self.emoji = emoji
        self.effect_sticker_id = effect_sticker_id
        self.sticker = sticker
        self.is_premium = is_premium
        self.static_icon_id = static_icon_id
        self.effect_animation_id = effect_animation_id

    @staticmethod
    async def _parse(
        client,
        effect: raw.types.AvailableEffect,
        document: raw.types.Document = None,
    ) -> AvailableEffect:
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
            effect_animation_id=getattr(effect, "effect_animation_id", None),
        )
