import asyncio
import logging

import pyrogram

log = logging.getLogger(__name__)


class Initialize:
    async def initialize(
        self: "pyrogram.Client",
    ):
        if not self.is_connected:
            raise ConnectionError("Can't initialize a disconnected client")

        if self.is_initialized:
            raise ConnectionError("Client is already initialized")

        self.load_plugins()

        await self.dispatcher.start()

        self.updates_watchdog_task = asyncio.create_task(self.updates_watchdog())

        self.is_initialized = True
