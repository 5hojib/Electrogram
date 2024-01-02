from pyrogram import raw
from .auto_name import AutoName

class MessagesFilter(AutoName):
    EMPTY = raw.types.InputMessagesFilterEmpty
    PHOTO = raw.types.InputMessagesFilterPhotos
    VIDEO = raw.types.InputMessagesFilterVideo
    PHOTO_VIDEO = raw.types.InputMessagesFilterPhotoVideo
    DOCUMENT = raw.types.InputMessagesFilterDocument
    URL = raw.types.InputMessagesFilterUrl
    ANIMATION = raw.types.InputMessagesFilterGif
    VOICE_NOTE = raw.types.InputMessagesFilterVoice
    VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo
    AUDIO_VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo
    AUDIO = raw.types.InputMessagesFilterMusic
    CHAT_PHOTO = raw.types.InputMessagesFilterChatPhotos
    PHONE_CALL = raw.types.InputMessagesFilterPhoneCalls
    MENTION = raw.types.InputMessagesFilterMyMentions
    LOCATION = raw.types.InputMessagesFilterGeo
    CONTACT = raw.types.InputMessagesFilterContacts
    PINNED = raw.types.InputMessagesFilterPinned
