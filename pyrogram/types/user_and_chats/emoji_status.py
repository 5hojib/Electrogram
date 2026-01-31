from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, utils
from pyrogram.types.object import Object

if TYPE_CHECKING:
    from datetime import datetime


class EmojiStatus(Object):
    """A user emoji status.

    Parameters:
        custom_emoji_id (``int``):
            Custom emoji id.

        until_date (:py:obj:`~datetime.datetime`, *optional*):
            Valid until date.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        custom_emoji_id: int,
        until_date: datetime | None = None,
    ) -> None:
        super().__init__(client)

        self.custom_emoji_id = custom_emoji_id
        self.until_date = until_date

    @staticmethod
    def _parse(client, emoji_status: raw.base.EmojiStatus) -> EmojiStatus | None:
        if isinstance(emoji_status, raw.types.EmojiStatus):
            return EmojiStatus(
                client=client,
                custom_emoji_id=emoji_status.document_id,
            )

        if isinstance(emoji_status, raw.types.EmojiStatusUntil):
            return EmojiStatus(
                client=client,
                custom_emoji_id=emoji_status.document_id,
                until_date=utils.timestamp_to_datetime(emoji_status.until),
            )

        return None

    def write(self):
        if self.until_date:
            return raw.types.EmojiStatusUntil(
                document_id=self.custom_emoji_id,
                until=utils.datetime_to_timestamp(self.until_date),
            )

        return raw.types.EmojiStatus(document_id=self.custom_emoji_id)
