from __future__ import annotations

from typing import Any

from .tl_object import TLObject


class List(list[Any], TLObject):
    def __repr__(self) -> str:
        return f"pyrogram.raw.core.List([{','.join(TLObject.__repr__(i) for i in self)}])"
