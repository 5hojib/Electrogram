from __future__ import annotations

import pyrogram
from pyrogram import raw

from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleAllowPremium(InputPrivacyRule):
    """Allow only users with a Premium subscription, currently only usable for :obj:`~pyrogram.enums.PrivacyKey.CHAT_INVITE`."""

    def __init__(
        self,
    ) -> None:
        super().__init__()

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ):
        return raw.types.InputPrivacyValueAllowPremium()
