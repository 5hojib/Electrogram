import pyrogram
from pyrogram import raw
from pyrogram import types


class CreateChannel:
    async def create_channel(
        self: "pyrogram.Client", title: str, description: str = ""
    ) -> "types.Chat":
        r = await self.invoke(
            raw.functions.channels.CreateChannel(
                title=title, about=description, broadcast=True
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
