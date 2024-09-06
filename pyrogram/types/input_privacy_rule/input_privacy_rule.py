from __future__ import annotations

from typing import TYPE_CHECKING, NoReturn

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram


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

    def __init__(self) -> None:
        super().__init__()

    async def write(self, client: pyrogram.Client) -> NoReturn:
        raise NotImplementedError
