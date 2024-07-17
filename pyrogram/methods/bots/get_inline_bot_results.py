from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram.errors import UnknownError


class GetInlineBotResults:
    async def get_inline_bot_results(
        self: "pyrogram.Client",
        bot: Union[int, str],
        query: str = "",
        offset: str = "",
        latitude: float = None,
        longitude: float = None,
    ):
        try:
            return await self.invoke(
                raw.functions.messages.GetInlineBotResults(
                    bot=await self.resolve_peer(bot),
                    peer=raw.types.InputPeerSelf(),
                    query=query,
                    offset=offset,
                    geo_point=raw.types.InputGeoPoint(lat=latitude, long=longitude)
                    if (latitude is not None and longitude is not None)
                    else None,
                )
            )
        except UnknownError as e:
            if e.value.error_code == -503 and e.value.error_message == "Timeout":
                raise TimeoutError("The inline bot didn't answer in time") from None
            else:
                raise e
