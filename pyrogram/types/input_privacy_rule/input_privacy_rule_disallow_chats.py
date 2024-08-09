import asyncio
from typing import Union, Iterable

import pyrogram
from pyrogram import raw, utils
from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleDisallowChats(InputPrivacyRule):
    """Disallow only participants of certain chats.

    Parameters:
        chat_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``):
            Unique identifier (int) or username (str) of the target chat.
    """

    def __init__(
        self,
        chat_ids: Union[int, str, Iterable[Union[int, str]]],
    ):
        super().__init__()

        self.chat_ids = chat_ids

    async def write(self, client: "pyrogram.Client"):
        chats = list(self.chat_ids) if not isinstance(self.chat_ids, (int, str)) else [self.chat_ids]
        chats = await asyncio.gather(*[client.resolve_peer(i) for i in chats])

        return raw.types.InputPrivacyValueDisallowChatParticipants(
            chats=[utils.get_peer_id(i) for i in chats]
        )
