from json import dumps
from random import randint
from typing import Union

import pyrogram
from pyrogram import raw, enums


class SendChatAction:
    async def send_chat_action(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        action: "enums.ChatAction",
        message_thread_id: int = None,
        emoji: str = None,
        emoji_message_id: int = None,
        emoji_message_interaction: "raw.types.DataJSON" = None
    ) -> bool:
        action_name = action.name.lower()

        if "upload" in action_name or "history" in action_name:
            action = action.value(progress=0)
        elif "watch_emoji" in action_name:
            if emoji is None:
                raise ValueError(
                    "Invalid Argument Provided"
                )
            action = action.value(emoticon=emoji)
        elif "trigger_emoji" in action_name:
            if (
                emoji is None or
                emoji_message_id is None
            ):
                raise ValueError(
                    "Invalid Argument Provided"
                )
            if emoji_message_interaction is None:
                _, sticker_set = await self._get_raw_stickers(
                    raw.types.InputStickerSetAnimatedEmojiAnimations()
                )
                emoji_message_interaction = raw.types.DataJSON(
                    data=dumps(
                        {
                            "v": 1,
                            "a":[
                                {
                                    "t": 0,
                                    "i": randint(
                                        1,
                                        sticker_set.count
                                    )
                                }
                            ]
                        }
                    )
                )
            action = action.value(
                emoticon=emoji,
                msg_id=emoji_message_id,
                interaction=emoji_message_interaction
            )
        else:
            action = action.value()
        rpc = raw.functions.messages.SetTyping(
            peer=await self.resolve_peer(chat_id),
            action=action,
            top_msg_id=message_thread_id
        )
        return await self.invoke(rpc)
