from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyrogram


class Disconnect:
    async def disconnect(
        self: pyrogram.Client,
    ) -> None:
        """Disconnect the client from Telegram servers.

        Raises:
            ConnectionError: In case you try to disconnect an already disconnected client or in case you try to
                disconnect a client that needs to be terminated first.
        """
        if not self.is_connected:
            raise ConnectionError("Client is already disconnected")

        if self.is_initialized:
            raise ConnectionError("Can't disconnect an initialized client")

        await self.session.stop()
        await self.storage.close()
        self.is_connected = False
