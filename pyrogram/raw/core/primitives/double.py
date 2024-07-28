from io import BytesIO
from struct import pack, unpack
from typing import Any, cast

from pyrogram.raw.core.tl_object import TLObject


class Double(bytes, TLObject):
    @classmethod
    def read(cls, data: BytesIO, *args: Any) -> float:
        return cast(float, unpack("d", data.read(8))[0])

    def __new__(cls, value: float) -> bytes:  # type: ignore
        return pack("d", value)
