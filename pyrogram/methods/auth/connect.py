import pyrogram
from pyrogram.session import Session


class Connect:
    async def connect(
        self: "pyrogram.Client",
    ) -> bool:
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
