from __future__ import annotations

from .copy_media_group import CopyMediaGroup
from .copy_message import CopyMessage
from .delete_chat_history import DeleteChatHistory
from .delete_messages import DeleteMessages
from .delete_scheduled_messages import DeleteScheduledMessages
from .download_media import DownloadMedia
from .edit_inline_caption import EditInlineCaption
from .edit_inline_media import EditInlineMedia
from .edit_inline_reply_markup import EditInlineReplyMarkup
from .edit_inline_text import EditInlineText
from .edit_message_caption import EditMessageCaption
from .edit_message_media import EditMessageMedia
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessageText
from .forward_messages import ForwardMessages
from .get_available_effects import GetAvailableEffects
from .get_chat_history import GetChatHistory
from .get_chat_history_count import GetChatHistoryCount
from .get_custom_emoji_stickers import GetCustomEmojiStickers
from .get_discussion_message import GetDiscussionMessage
from .get_discussion_replies import GetDiscussionReplies
from .get_discussion_replies_count import GetDiscussionRepliesCount
from .get_media_group import GetMediaGroup
from .get_messages import GetMessages
from .get_scheduled_messages import GetScheduledMessages
from .read_chat_history import ReadChatHistory
from .retract_vote import RetractVote
from .search_global import SearchGlobal
from .search_global_count import SearchGlobalCount
from .search_global_hashtag_messages import SearchGlobalHashtagMessages
from .search_global_hashtag_messages_count import SearchGlobalHashtagMessagesCount
from .search_messages import SearchMessages
from .search_messages_count import SearchMessagesCount
from .send_animation import SendAnimation
from .send_audio import SendAudio
from .send_cached_media import SendCachedMedia
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_dice import SendDice
from .send_document import SendDocument
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_paid_media import SendPaidMedia
from .send_paid_reaction import SendPaidReaction
from .send_photo import SendPhoto
from .send_poll import SendPoll
from .send_reaction import SendReaction
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice
from .send_web_page import SendWebPage
from .stop_poll import StopPoll
from .stream_media import StreamMedia
from .translate_text import TranslateText
from .vote_poll import VotePoll


class Messages(
    DeleteChatHistory,
    DeleteMessages,
    DeleteScheduledMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageMedia,
    EditMessageText,
    ForwardMessages,
    GetAvailableEffects,
    GetMediaGroup,
    GetMessages,
    GetScheduledMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SendAnimation,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice,
    SendWebPage,
    SendPaidMedia,
    SendPaidReaction,
    SendPoll,
    TranslateText,
    VotePoll,
    StopPoll,
    RetractVote,
    DownloadMedia,
    GetChatHistory,
    SendCachedMedia,
    GetChatHistoryCount,
    ReadChatHistory,
    EditInlineText,
    EditInlineCaption,
    EditInlineMedia,
    EditInlineReplyMarkup,
    SendDice,
    SearchMessages,
    SearchGlobal,
    SearchGlobalHashtagMessages,
    CopyMessage,
    CopyMediaGroup,
    SearchMessagesCount,
    SearchGlobalCount,
    SearchGlobalHashtagMessagesCount,
    GetDiscussionMessage,
    SendReaction,
    GetDiscussionReplies,
    GetDiscussionRepliesCount,
    StreamMedia,
    GetCustomEmojiStickers,
):
    pass
