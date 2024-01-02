from typing import List

import pyrogram
from pyrogram import raw, types


class GetBotCommands:
    async def get_bot_commands(
        self: "pyrogram.Client",
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ) -> List["types.BotCommand"]:
        r = await self.invoke(
            raw.functions.bots.GetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )

        return types.List(types.BotCommand.read(c) for c in r)
