from __future__ import annotations

from typing import TYPE_CHECKING, Any

from pyrogram.raw.core.tl_object import TLObject

if TYPE_CHECKING:
    from io import BytesIO


class Bytes(bytes, TLObject):
    @classmethod
    def read(cls, data: BytesIO, *args: Any) -> bytes:  # noqa: ARG003
        length = int.from_bytes(data.read(1), "little")

        if length <= 253:
            x = data.read(length)
            data.read(-(length + 1) % 4)
        else:
            length = int.from_bytes(data.read(3), "little")
            x = data.read(length)
            data.read(-length % 4)

        return x

    def __new__(cls, value: bytes) -> bytes:  # type: ignore
        length = len(value)

        if length <= 253:
            return bytes([length]) + value + bytes(-(length + 1) % 4)
        return (
            bytes([254]) + length.to_bytes(3, "little") + value + bytes(-length % 4)
        )
