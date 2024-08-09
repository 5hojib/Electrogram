import pyrogram
from pyrogram import raw
from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleAllowContacts(InputPrivacyRule):
    """Allow contacts only."""

    def __init__(
        self,
    ):
        super().__init__()

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputPrivacyValueAllowContacts()
