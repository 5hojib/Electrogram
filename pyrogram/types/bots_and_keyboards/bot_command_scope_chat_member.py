from typing import Union

import pyrogram
from pyrogram import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeChatMember(BotCommandScope):
    def __init__(self, chat_id: Union[int, str], user_id: Union[int, str]):
        super().__init__("chat_member")

        self.chat_id = chat_id
        self.user_id = user_id

    async def write(self, client: "pyrogram.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopePeerUser(
            peer=await client.resolve_peer(self.chat_id),
            user_id=await client.resolve_peer(self.user_id),
        )
