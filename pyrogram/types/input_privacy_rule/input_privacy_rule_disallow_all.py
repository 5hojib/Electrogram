import pyrogram
from pyrogram import raw
from .input_privacy_rule import InputPrivacyRule


class InputPrivacyRuleDisallowAll(InputPrivacyRule):
    """Disallow all users."""

    def __init__(
        self,
    ):
        super().__init__()

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputPrivacyValueDisallowAll()
