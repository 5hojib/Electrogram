from __future__ import annotations

from .get_account_ttl import GetAccountTTL
from .set_account_ttl import SetAccountTTL


class Account(GetAccountTTL, SetAccountTTL):
    pass
