from typing import Union, List

import pyrogram
from pyrogram import raw, types


class SendReaction:
    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        story_id: int = None,
        emoji: Union[int, str, List[Union[int, str]]] = None,
        big: bool = False,
        add_to_recent: bool = False,
    ) -> "types.MessageReactions":
        if isinstance(emoji, list):
            reaction = (
                [
                    raw.types.ReactionCustomEmoji(document_id=i)
                    if isinstance(i, int)
                    else raw.types.ReactionEmoji(emoticon=i)
                    for i in emoji
                ]
                if emoji
                else None
            )
        else:
            if isinstance(emoji, int):
                reaction = [raw.types.ReactionCustomEmoji(document_id=emoji)]
            else:
                reaction = [raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None
        if message_id is not None:
            r = await self.invoke(
                raw.functions.messages.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    msg_id=message_id,
                    reaction=reaction,
                    big=big,
                    add_to_recent=add_to_recent,
                )
            )
            for i in r.updates:
                if isinstance(i, raw.types.UpdateMessageReactions):
                    return types.MessageReactions._parse(self, i.reactions)
        elif story_id is not None:
            await self.invoke(
                raw.functions.stories.SendReaction(
                    peer=await self.resolve_peer(chat_id),
                    story_id=story_id,
                    reaction=raw.types.ReactionEmoji(emoticon=emoji) if emoji else None,
                    add_to_recent=add_to_recent,
                )
            )
            return True
        else:
            raise ValueError("You need to pass one of message_id!")
