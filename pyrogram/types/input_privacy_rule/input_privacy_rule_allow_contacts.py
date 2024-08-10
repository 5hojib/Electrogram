from __future__ import annotations

import pyrogram
from pyrogram import raw

from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleAllowContacts(InputPrivacyRule):
    """Allow contacts only."""

    def __init__(
        self,
    ):
        super().__init__()

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ):
        return raw.types.InputPrivacyValueAllowContacts()
