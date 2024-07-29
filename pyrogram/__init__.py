__version__ = "v2.184.0"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


crypto_executor = ThreadPoolExecutor(
    1, thread_name_prefix="CryptoWorker"
)

# ruff: noqa: E402
import asyncio
from contextlib import suppress

import uvloop

from . import enums, errors, filters, handlers, raw, types
from .client import Client
from .sync import compose, idle

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


__all__ = [
    "Client",
    "ContinuePropagation",
    "StopPropagation",
    "StopTransmission",
    "compose",
    "crypto_executor",
    "enums",
    "errors",
    "filters",
    "handlers",
    "idle",
    "raw",
    "types",
]
