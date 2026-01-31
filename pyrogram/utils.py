from __future__ import annotations

import asyncio
import functools
import hashlib
import os
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timezone
from getpass import getpass
from typing import TYPE_CHECKING, Any, TypeVar

from pyrogram import raw

if TYPE_CHECKING:
    from collections.abc import Callable

MIN_CHANNEL_ID = -1007852516352
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -999999999999
MAX_USER_ID = 999999999999


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def get_raw_peer_id(
    peer: raw.base.Peer | raw.base.RequestedPeer,
) -> int | None:
    """Get the raw peer id from a Peer object"""
    if isinstance(peer, (raw.types.PeerUser, raw.types.RequestedPeerUser)):
        return peer.user_id

    if isinstance(peer, (raw.types.PeerChat, raw.types.RequestedPeerChat)):
        return peer.chat_id

    if isinstance(peer, (raw.types.PeerChannel, raw.types.RequestedPeerChannel)):
        return peer.channel_id

    return None


def get_peer_id(peer: raw.base.Peer) -> int:
    """Get the non-raw peer id from a Peer object"""
    if isinstance(peer, raw.types.PeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat):
        return -peer.chat_id

    if isinstance(peer, raw.types.PeerChannel):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError(f"Peer type invalid: {peer}")


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if peer_id >= MIN_CHAT_ID:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id


def btoi(b: bytes) -> int:
    return int.from_bytes(b, "big")


def itob(i: int) -> bytes:
    return i.to_bytes(256, "big")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b, strict=False))


def compute_password_hash(
    algo: raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow,
    password: str,
) -> bytes:
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1)
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2)


def compute_password_check(
    r: raw.types.account.Password,
    password: str,
) -> raw.types.InputCheckPasswordSRP:
    algo = r.current_algo

    p_bytes = algo.p
    p = btoi(algo.p)

    g_bytes = itob(algo.g)
    g = algo.g

    B_bytes = r.srp_B
    B = btoi(B_bytes)

    srp_id = r.srp_id

    x_bytes = compute_password_hash(algo, password)
    x = btoi(x_bytes)

    g_x = pow(g, x, p)

    k_bytes = sha256(p_bytes + g_bytes)
    k = btoi(k_bytes)

    kg_x = (k * g_x) % p

    while True:
        a_bytes = os.urandom(256)
        a = btoi(a_bytes)

        A = pow(g, a, p)
        A_bytes = itob(A)

        u = btoi(sha256(A_bytes + B_bytes))

        if u > 0:
            break

    g_b = (B - kg_x) % p

    ux = u * x
    a_ux = a + ux
    S = pow(g_b, a_ux, p)
    S_bytes = itob(S)

    K_bytes = sha256(S_bytes)

    M1_bytes = sha256(
        xor(sha256(p_bytes), sha256(g_bytes))
        + sha256(algo.salt1)
        + sha256(algo.salt2)
        + A_bytes
        + B_bytes
        + K_bytes,
    )

    return raw.types.InputCheckPasswordSRP(srp_id=srp_id, A=A_bytes, M1=M1_bytes)


def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def timestamp_to_datetime(ts: int | None) -> datetime | None:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: datetime | None) -> int | None:
    return int(dt.timestamp()) if dt else None


async def run_sync(
    func: Callable[..., TypeVar("Result")],
    *args: Any,
    **kwargs: Any,
) -> TypeVar("Result"):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))
