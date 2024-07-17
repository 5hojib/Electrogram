import logging
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetAvailableEffects:
    async def get_available_effects(
        self: "pyrogram.Client",
    ) -> List["types.AvailableEffect"]:
        r = await self.invoke(raw.functions.messages.GetAvailableEffects(hash=0))

        documents = {d.id: d for d in r.documents}

        return types.List(
            [
                await types.AvailableEffect._parse(
                    self, effect, documents.get(effect.effect_sticker_id, None)
                )
                for effect in r.effects
            ]
        )
