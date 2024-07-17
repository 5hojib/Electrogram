from typing import Union

import pyrogram
from pyrogram import raw


class GetBotInfo:
    async def get_bot_info(
        self: "pyrogram.Client", lang_code: str, bot: Union[int, str] = None
    ) -> pyrogram.types.BotInfo:
        peer = None
        if bot:
            peer = await self.resolve_peer(bot)
        r = await self.invoke(
            raw.functions.bots.GetBotInfo(lang_code=lang_code, bot=peer)
        )
        return pyrogram.types.BotInfo._parse(r)
