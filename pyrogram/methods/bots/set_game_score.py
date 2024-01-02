from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class SetGameScore:
    async def set_game_score(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        score: int,
        force: bool = None,
        disable_edit_message: bool = None,
        chat_id: Union[int, str] = None,
        message_id: int = None
    ) -> Union["types.Message", bool]:
        r = await self.invoke(
            raw.functions.messages.SetGameScore(
                peer=await self.resolve_peer(chat_id),
                score=score,
                id=message_id,
                user_id=await self.resolve_peer(user_id),
                force=force or None,
                edit_message=not disable_edit_message or None
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateEditMessage,
                              raw.types.UpdateEditChannelMessage)):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

        return True
