#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.

__version__ = "1.184.0"
__license__ = "MIT License"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(Exception):  # noqa: N818
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

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
