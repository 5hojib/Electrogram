from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.session import Session

if TYPE_CHECKING:
    import pyrogram


class Connect:
    async def connect(
        self: pyrogram.Client,
    ) -> bool:
        """
        Connect the client to Telegram servers.

        Returns:
            ``bool``: On success, in case the passed-in session is authorized, True is returned. Otherwise, in case
            the session needs to be authorized, False is returned.

        Raises:
            ConnectionError: In case you try to connect an already connected client.
        """
        if self.is_connected:
            raise ConnectionError("Client is already connected")

        await self.load_session()

        self.session = Session(
            self,
            await self.storage.dc_id(),
            await self.storage.auth_key(),
            await self.storage.test_mode(),
        )

        await self.session.start()

        self.is_connected = True

        return bool(await self.storage.user_id())
