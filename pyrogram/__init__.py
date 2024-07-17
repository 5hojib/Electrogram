__version__ = "v1.184.3"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):  # noqa: N818
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


# ruff: noqa: E402
from . import enums, errors, filters, handlers, raw, types
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

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
