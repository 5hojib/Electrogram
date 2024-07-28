__version__ = "1.184.0"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):  # noqa: N818
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


crypto_executor = ThreadPoolExecutor(
    1, thread_name_prefix="CryptoWorker"
)

# ruff: noqa: E402
import asyncio as _asyncio
from contextlib import suppress

from . import enums, errors, filters, handlers, raw, types
from .client import Client
from .methods.utilities.compose import compose
from .methods.utilities.idle import idle

with suppress(ImportError):
    import uvloop as _uvloop

    _asyncio.set_event_loop_policy(_uvloop.EventLoopPolicy())


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
