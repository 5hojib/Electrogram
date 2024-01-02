from typing import Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types


class AnswerInlineQuery:
    async def answer_inline_query(
        self: "pyrogram.Client",
        inline_query_id: str,
        results: Iterable["types.InlineQueryResult"],
        cache_time: int = 300,
        is_gallery: bool = False,
        is_personal: bool = False,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        return await self.invoke(
            raw.functions.messages.SetInlineBotResults(
                query_id=int(inline_query_id),
                results=[await r.write(self) for r in results],
                cache_time=cache_time,
                gallery=is_gallery or None,
                private=is_personal or None,
                next_offset=next_offset or None,
                switch_pm=raw.types.InlineBotSwitchPM(
                    text=switch_pm_text,
                    start_param=switch_pm_parameter
                ) if switch_pm_text else None
            )
        )
