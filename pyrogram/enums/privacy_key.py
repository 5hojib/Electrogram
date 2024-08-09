from __future__ import annotations

from pyrogram import raw

from .auto_name import AutoName


class PrivacyKey(AutoName):
    """Privacy key enumeration used in :meth:`~pyrogram.Client.set_privacy`."""

    ABOUT = raw.types.InputPrivacyKeyAbout
    "Whether people can see your bio"

    ADDED_BY_PHONE = raw.types.InputPrivacyKeyAddedByPhone
    "Whether people can add you to their contact list by your phone number"

    BIRTHDAY = raw.types.InputPrivacyKeyBirthday
    "Whether the user can see our birthday."

    CHAT_INVITE = raw.types.InputPrivacyKeyChatInvite
    "Whether people will be able to invite you to chats"

    FORWARDS = raw.types.InputPrivacyKeyForwards
    "Whether messages forwarded from you will be anonymous"

    PHONE_CALL = raw.types.InputPrivacyKeyPhoneCall
    "Whether you will accept phone calls"

    PHONE_NUMBER = raw.types.InputPrivacyKeyPhoneNumber
    "Whether people will be able to see your phone number"

    PHONE_P2P = raw.types.InputPrivacyKeyPhoneP2P
    "Whether to allow P2P communication during VoIP calls"

    PROFILE_PHOTO = raw.types.InputPrivacyKeyProfilePhoto
    "Whether people will be able to see your profile picture"

    STATUS = raw.types.InputPrivacyKeyStatusTimestamp
    "Whether people will be able to see our exact last online timestamp."

    VOICE_MESSAGES = raw.types.InputPrivacyKeyVoiceMessages
    "Whether people can send you voice messages or round videos (Premium users only)."
