import asyncio
from typing import Union, Iterable

import pyrogram
from pyrogram import raw
from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleAllowUsers(InputPrivacyRule):
    """Allow only participants of certain users.

    Parameters:
        chat_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``, *optional*):
            Unique identifier (int) or username (str) of the target chat.
    """

    def __init__(
        self,
        chat_ids: Union[int, str, Iterable[Union[int, str]]],
    ):
        super().__init__()

        self.chat_ids = chat_ids

    async def write(self, client: "pyrogram.Client"):
        users = list(self.chat_ids) if not isinstance(self.chat_ids, (int, str)) else [self.chat_ids]
        users = await asyncio.gather(*[client.resolve_peer(i) for i in users])

        return raw.types.InputPrivacyValueAllowUsers(users=users)
