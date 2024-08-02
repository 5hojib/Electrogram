from __future__ import annotations

from .add_sticker_to_set import AddStickerToSet
from .create_sticker_set import CreateStickerSet
from .get_sticker_set import GetStickerSet


class Stickers(AddStickerToSet, CreateStickerSet, GetStickerSet):
    pass
