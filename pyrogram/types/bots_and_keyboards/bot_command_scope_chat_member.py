from __future__ import annotations

import pyrogram
from pyrogram import raw

from .bot_command_scope import BotCommandScope


class BotCommandScopeChatMember(BotCommandScope):
    """Represents the scope of bot commands, covering a specific member of a group or supergroup chat.

    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup (in the format
            @supergroupusername).

        user_id (``int`` | ``str``):
            Unique identifier of the target user.
    """

    def __init__(self, chat_id: int | str, user_id: int | str) -> None:
        super().__init__("chat_member")

        self.chat_id = chat_id
        self.user_id = user_id

    async def write(self, client: pyrogram.Client) -> raw.base.BotCommandScope:
        return raw.types.BotCommandScopePeerUser(
            peer=await client.resolve_peer(self.chat_id),
            user_id=await client.resolve_peer(self.user_id),
        )
