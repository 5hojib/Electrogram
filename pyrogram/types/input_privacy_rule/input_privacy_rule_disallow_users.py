from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw

from .input_privacy_rule import InputPrivacyRule

if TYPE_CHECKING:
    from collections.abc import Iterable


class InputPrivacyRuleDisallowUsers(InputPrivacyRule):
    """Disallow only participants of certain users.

    Parameters:
        chat_ids (``int`` | ``str`` | Iterable of ``int`` or ``str``, *optional*):
            Unique identifier (int) or username (str) of the target chat.
    """

    def __init__(
        self,
        chat_ids: int | str | Iterable[int | str],
    ) -> None:
        super().__init__()

        self.chat_ids = chat_ids

    async def write(self, client: pyrogram.Client):
        users = (
            list(self.chat_ids)
            if not isinstance(self.chat_ids, int | str)
            else [self.chat_ids]
        )
        users = await asyncio.gather(*[client.resolve_peer(i) for i in users])

        return raw.types.InputPrivacyValueDisallowUsers(users=users)
