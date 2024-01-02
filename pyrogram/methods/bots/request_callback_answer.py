from typing import Union

import pyrogram
from pyrogram import raw


class RequestCallbackAnswer:
    async def request_callback_answer(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
        callback_data: Union[str, bytes],
        timeout: int = 10
    ):
        data = bytes(callback_data, "utf-8") if isinstance(callback_data, str) else callback_data

        return await self.invoke(
            raw.functions.messages.GetBotCallbackAnswer(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                data=data
            ),
            retries=0,
            timeout=timeout
        )
