import inspect
from collections.abc import Callable
from typing import TYPE_CHECKING

from pyrogram.filters import Filter
from pyrogram.types import Update

if TYPE_CHECKING:
    import pyrogram


class Handler:
    def __init__(
        self, callback: Callable, filters: Filter = None
    ) -> None:
        self.callback = callback
        self.filters = filters

    async def check(self, client: "pyrogram.Client", update: Update):
        if callable(self.filters):
            if inspect.iscoroutinefunction(self.filters.__call__):
                return await self.filters(client, update)
            return await client.loop.run_in_executor(
                client.executor, self.filters, client, update
            )

        return True
