from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyrogram.raw.core.tl_object import TLObject

if TYPE_CHECKING:
    from io import BytesIO


class BoolFalse(bytes, TLObject):
    ID = 0xBC799737
    value = False

    @classmethod
    def read(cls, *args: Any) -> bool:  # noqa: ARG003
        return cls.value

    def __new__(cls) -> bytes:  # type: ignore
        return cls.ID.to_bytes(4, "little")


class BoolTrue(BoolFalse):
    ID = 0x997275B5
    value = True


class Bool(bytes, TLObject):
    @classmethod
    def read(cls, data: BytesIO, *args: Any) -> bool:  # noqa: ARG003
        return int.from_bytes(data.read(4), "little") == BoolTrue.ID

    def __new__(cls, value: bool) -> bytes:  # type: ignore
        return BoolTrue() if value else BoolFalse()
