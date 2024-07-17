import asyncio
from typing import List

import pyrogram
from .idle import idle


async def compose(clients: List["pyrogram.Client"], sequential: bool = False):
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
