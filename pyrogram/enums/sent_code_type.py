from pyrogram import raw
from .auto_name import AutoName

class SentCodeType(AutoName):
    APP = raw.types.auth.SentCodeTypeApp
    CALL = raw.types.auth.SentCodeTypeCall
    FLASH_CALL = raw.types.auth.SentCodeTypeFlashCall
    MISSED_CALL = raw.types.auth.SentCodeTypeMissedCall
    SMS = raw.types.auth.SentCodeTypeSms
    FRAGMENT_SMS = raw.types.auth.SentCodeTypeFragmentSms
    EMAIL_CODE = raw.types.auth.SentCodeTypeEmailCode
