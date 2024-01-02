from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram import types


class VotePoll:
    async def vote_poll(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: id,
        options: Union[int, List[int]]
    ) -> "types.Poll":
        poll = (await self.get_messages(chat_id, message_id)).poll
        options = [options] if not isinstance(options, list) else options

        r = await self.invoke(
            raw.functions.messages.SendVote(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[poll.options[option].data for option in options]
            )
        )

        return types.Poll._parse(self, r.updates[0])
