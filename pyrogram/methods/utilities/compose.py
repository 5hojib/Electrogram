from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyrogram

from .idle import idle


async def compose(clients: list[pyrogram.Client], sequential: bool = False) -> None:
    """Run multiple clients at once.

    This method can be used to run multiple clients at once and can be found directly in the ``pyrogram`` package.

    If you want to run a single client, you can use Client's bound method :meth:`~pyrogram.Client.run`.

    Parameters:
        clients (List of :obj:`~pyrogram.Client`):
            A list of client objects to run.

        sequential (``bool``, *optional*):
            Pass True to run clients sequentially.
            Defaults to False (run clients concurrently)

    Example:
        .. code-block:: python

            import asyncio
            from pyrogram import Client, compose


            async def main():
                apps = [
                    Client("account1"),
                    Client("account2"),
                    Client("account3")
                ]

                ...

                await compose(apps)


            asyncio.run(main())

    """
    if sequential:
        for c in clients:
            await c.start()
    else:
        await asyncio.gather(*[c.start() for c in clients])

    await idle()

    if sequential:
        for c in clients:
            await c.stop()
    else:
        await asyncio.gather(*[c.stop() for c in clients])
