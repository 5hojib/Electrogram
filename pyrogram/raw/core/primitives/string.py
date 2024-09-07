from __future__ import annotations

from typing import TYPE_CHECKING, cast

from .bytes import Bytes

if TYPE_CHECKING:
    from io import BytesIO


class String(Bytes):
    @classmethod
    def read(cls, data: BytesIO, *args) -> str:  # noqa: ARG003
        return cast(bytes, super(String, String).read(data)).decode(errors="replace")

    def __new__(cls, value: str) -> bytes:
        return super().__new__(cls, value.encode())
