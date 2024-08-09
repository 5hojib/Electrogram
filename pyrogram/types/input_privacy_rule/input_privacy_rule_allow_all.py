import pyrogram
from pyrogram import raw
from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleAllowAll(InputPrivacyRule):
    """Allow all users."""

    def __init__(
        self,
    ):
        super().__init__()

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputPrivacyValueAllowAll()
