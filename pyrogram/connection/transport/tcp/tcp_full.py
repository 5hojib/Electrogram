# ruff: noqa: ARG002
from __future__ import annotations

import logging
from binascii import crc32
from struct import pack, unpack

from .tcp import TCP, Proxy

log = logging.getLogger(__name__)


class TCPFull(TCP):
    def __init__(self, ipv6: bool, proxy: Proxy) -> None:
        super().__init__(ipv6, proxy)

        self.seq_no: int | None = None

    async def connect(self, address: tuple[str, int]) -> None:
        await super().connect(address)
        self.seq_no = 0

    async def send(self, data: bytes, *args) -> None:
        data = pack("<II", len(data) + 12, self.seq_no) + data
        data += pack("<I", crc32(data))
        self.seq_no += 1

        await super().send(data)

    async def recv(self, length: int = 0) -> bytes | None:
        length = await super().recv(4)

        if length is None:
            return None

        packet = await super().recv(unpack("<I", length)[0] - 4)

        if packet is None:
            return None

        packet = length + packet
        checksum = packet[-4:]
        packet = packet[:-4]

        if crc32(packet) != unpack("<I", checksum)[0]:
            return None

        return packet[8:]
