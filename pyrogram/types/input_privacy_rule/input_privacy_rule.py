import pyrogram

from ..object import Object


class InputPrivacyRule(Object):
    """Content of a privacy rule.

    It should be one of:

    - :obj:`~pyrogram.types.InputPrivacyRuleAllowAll`
    - :obj:`~pyrogram.types.InputPrivacyRuleAllowContacts`
    - :obj:`~pyrogram.types.InputPrivacyRuleAllowPremium`
    - :obj:`~pyrogram.types.InputPrivacyRuleAllowUsers`
    - :obj:`~pyrogram.types.InputPrivacyRuleAllowChats`
    - :obj:`~pyrogram.types.InputPrivacyRuleDisallowAll`
    - :obj:`~pyrogram.types.InputPrivacyRuleDisallowContacts`
    - :obj:`~pyrogram.types.InputPrivacyRuleDisallowUsers`
    - :obj:`~pyrogram.types.InputPrivacyRuleDisallowChats`
    """

    def __init__(self):
        super().__init__()

    async def write(self, client: "pyrogram.Client"):
        raise NotImplementedError
