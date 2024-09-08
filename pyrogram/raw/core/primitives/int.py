from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyrogram.raw.core.tl_object import TLObject

if TYPE_CHECKING:
    from io import BytesIO


class Int(bytes, TLObject):
    SIZE = 4

    @classmethod
    def read(
        cls,
        data: BytesIO,
        signed: bool = True,
        *args: Any,  # noqa: ARG003
    ) -> int:
        return int.from_bytes(data.read(cls.SIZE), "little", signed=signed)

    def __new__(cls, value: int, signed: bool = True) -> bytes:
        return value.to_bytes(cls.SIZE, "little", signed=signed)


class Long(Int):
    SIZE = 8


class Int128(Int):
    SIZE = 16


class Int256(Int):
    SIZE = 32
