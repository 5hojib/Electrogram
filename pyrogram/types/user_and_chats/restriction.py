from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class Restriction(Object):
    """A restriction applied to bots or chats.

    Parameters:
        platform (``str``):
            The platform the restriction is applied to, e.g. "ios", "android"

        reason (``str``):
            The restriction reason, e.g. "porn", "copyright".

        text (``str``):
            The restriction text.
    """

    def __init__(self, *, platform: str, reason: str, text: str) -> None:
        super().__init__(None)

        self.platform = platform
        self.reason = reason
        self.text = text

    @staticmethod
    def _parse(
        restriction: raw.types.RestrictionReason,
    ) -> Restriction:
        return Restriction(
            platform=restriction.platform,
            reason=restriction.reason,
            text=restriction.text,
        )
