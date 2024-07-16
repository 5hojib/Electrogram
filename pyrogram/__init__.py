__version__ = "v1.184.3"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor

class StopTransmission(Exception):
    pass

class StopPropagation(StopAsyncIteration):
    pass

class ContinuePropagation(StopAsyncIteration):
    pass

from . import raw, types, filters, handlers, emoji, enums
from .client import Client
from .sync import idle, compose

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

__all__ = [
    "__version__",
    "__license__",
    "StopTransmission",
    "StopPropagation",
    "ContinuePropagation",
    "raw",
    "types",
    "filters",
    "handlers",
    "emoji",
    "enums",
    "Client",
    "idle",
    "compose",
    "crypto_executor"
]