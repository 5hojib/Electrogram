from __future__ import annotations

from .get_account_ttl import GetAccountTTL
from .set_account_ttl import SetAccountTTL
from .get_privacy import GetPrivacy
from .set_privacy import SetPrivacy

class Account(GetAccountTTL, SetAccountTTL, GetPrivacy, SetPrivacy):
    pass
