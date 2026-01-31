from __future__ import annotations

from typing import Any, Callable
import pyrogram

class Filter:
    async def __call__(self, client: pyrogram.Client, update: Any) -> bool:
        raise NotImplementedError

    def __invert__(self):
        return InvertFilter(self)

    def __and__(self, other):
        return AndFilter(self, other)

    def __or__(self, other):
        return OrFilter(self, other)


class InvertFilter(Filter):
    def __init__(self, base):
        self.base = base

    async def __call__(self, client: pyrogram.Client, update: Any) -> bool:
        return not await self.base(client, update)


class AndFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: pyrogram.Client, update: Any) -> bool:
        return await self.base(client, update) and await self.other(client, update)


class OrFilter(Filter):
    def __init__(self, base, other):
        self.base = base
        self.other = other

    async def __call__(self, client: pyrogram.Client, update: Any) -> bool:
        return await self.base(client, update) or await self.other(client, update)


def create(func: Callable, **kwargs) -> Filter:
    return type(
        "Filter",
        (Filter,),
        {"__call__": lambda self, client, update: func(self, client, update, **kwargs)},
    )()
