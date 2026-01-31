from __future__ import annotations

from pyrogram import raw

from .auto_name import AutoName


class ChatAction(AutoName):
    """Chat action enumeration used in :obj:`~pyrogram.types.ChatEvent`."""

    TYPING = raw.types.SendMessageTypingAction
    "Typing text message"

    UPLOAD_PHOTO = raw.types.SendMessageUploadPhotoAction
    "Uploading photo"

    RECORD_VIDEO = raw.types.SendMessageRecordVideoAction
    "Recording video"

    UPLOAD_VIDEO = raw.types.SendMessageUploadVideoAction
    "Uploading video"

    RECORD_AUDIO = raw.types.SendMessageRecordAudioAction
    "Recording audio"

    UPLOAD_AUDIO = raw.types.SendMessageUploadAudioAction
    "Uploading audio"

    UPLOAD_DOCUMENT = raw.types.SendMessageUploadDocumentAction
    "Uploading document"

    FIND_LOCATION = raw.types.SendMessageGeoLocationAction
    "Finding location"

    RECORD_VIDEO_NOTE = raw.types.SendMessageRecordRoundAction
    "Recording video note"

    UPLOAD_VIDEO_NOTE = raw.types.SendMessageUploadRoundAction
    "Uploading video note"

    PLAYING = raw.types.SendMessageGamePlayAction
    "Playing game"

    CHOOSE_CONTACT = raw.types.SendMessageChooseContactAction
    "Choosing contact"

    SPEAKING = raw.types.SpeakingInGroupCallAction
    "Speaking in group call"

    IMPORT_HISTORY = raw.types.SendMessageHistoryImportAction
    "Importing history"

    CHOOSE_STICKER = raw.types.SendMessageChooseStickerAction
    "Choosing sticker"

    CANCEL = raw.types.SendMessageCancelAction
    "Cancel ongoing chat action"

    TRIGGER_EMOJI_ANIMATION = raw.types.SendMessageEmojiInteraction
    "User has clicked on an animated emoji triggering a `reaction <https://core.telegram.org/api/animated-emojis#emoji-reactions>`_"

    WATCH_EMOJI_ANIMATION = raw.types.SendMessageEmojiInteractionSeen
    "The user is watching animations sent by the other party by clicking on an animated emoji"
