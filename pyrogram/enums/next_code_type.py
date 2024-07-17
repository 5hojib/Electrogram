from pyrogram import raw
from .auto_name import AutoName


class NextCodeType(AutoName):
    CALL = raw.types.auth.CodeTypeCall
    FLASH_CALL = raw.types.auth.CodeTypeFlashCall
    MISSED_CALL = raw.types.auth.CodeTypeMissedCall
    SMS = raw.types.auth.CodeTypeSms
    FRAGMENT_SMS = raw.types.auth.CodeTypeFragmentSms
