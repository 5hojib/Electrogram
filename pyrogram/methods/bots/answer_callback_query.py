import pyrogram
from pyrogram import raw


class AnswerCallbackQuery:
    async def answer_callback_query(
        self: "pyrogram.Client",
        callback_query_id: str,
        text: str = None,
        show_alert: bool = None,
        url: str = None,
        cache_time: int = 0,
    ):
        return await self.invoke(
            raw.functions.messages.SetBotCallbackAnswer(
                query_id=int(callback_query_id),
                cache_time=cache_time,
                alert=show_alert or None,
                message=text or None,
                url=url or None,
            )
        )
