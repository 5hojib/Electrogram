# ruff: noqa: ARG002
from __future__ import annotations

import logging
from struct import pack, unpack

from .tcp import TCP, Proxy

log = logging.getLogger(__name__)


class TCPIntermediate(TCP):
    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        super().__init__(ipv6, proxy)

    async def connect(self, address: tuple[str, int]) -> None:
        await super().connect(address)
        await super().send(b"\xee" * 4)

    async def send(self, data: bytes, *args) -> None:
        await super().send(pack("<i", len(data)) + data)

    async def recv(self, length: int = 0) -> bytes | None:
        length = await super().recv(4)

        if length is None:
            return None

        return await super().recv(unpack("<i", length)[0])
