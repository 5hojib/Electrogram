from __future__ import annotations

from .input_privacy_rule import InputPrivacyRule
from .input_privacy_rule_allow_all import InputPrivacyRuleAllowAll
from .input_privacy_rule_allow_chats import InputPrivacyRuleAllowChats
from .input_privacy_rule_allow_contacts import InputPrivacyRuleAllowContacts
from .input_privacy_rule_allow_premium import InputPrivacyRuleAllowPremium
from .input_privacy_rule_allow_users import InputPrivacyRuleAllowUsers
from .input_privacy_rule_disallow_all import InputPrivacyRuleDisallowAll
from .input_privacy_rule_disallow_chats import InputPrivacyRuleDisallowChats
from .input_privacy_rule_disallow_contacts import InputPrivacyRuleDisallowContacts
from .input_privacy_rule_disallow_users import InputPrivacyRuleDisallowUsers

__all__ = [
    "InputPrivacyRule",
    "InputPrivacyRuleAllowAll",
    "InputPrivacyRuleAllowChats",
    "InputPrivacyRuleAllowContacts",
    "InputPrivacyRuleAllowPremium",
    "InputPrivacyRuleAllowUsers",
    "InputPrivacyRuleDisallowAll",
    "InputPrivacyRuleDisallowChats",
    "InputPrivacyRuleDisallowContacts",
    "InputPrivacyRuleDisallowUsers",
]
