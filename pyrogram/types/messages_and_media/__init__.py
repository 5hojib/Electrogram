from __future__ import annotations

from .animation import Animation
from .audio import Audio
from .available_effect import AvailableEffect
from .contact import Contact
from .contact_registered import ContactRegistered
from .dice import Dice
from .document import Document
from .exported_story_link import ExportedStoryLink
from .game import Game
from .gifted_premium import GiftedPremium
from .giveaway import Giveaway
from .giveaway_launched import GiveawayLaunched
from .giveaway_result import GiveawayResult
from .labeled_price import LabeledPrice
from .location import Location
from .media_area import MediaArea
from .media_area_channel_post import MediaAreaChannelPost
from .media_area_coordinates import MediaAreaCoordinates
from .message import Message
from .message_entity import MessageEntity
from .message_reaction_count_updated import (
    MessageReactionCountUpdated,
)
from .message_reaction_updated import MessageReactionUpdated
from .message_reactions import MessageReactions
from .message_story import MessageStory
from .payment_form import PaymentForm
from .photo import Photo
from .poll import Poll
from .poll_option import PollOption
from .reaction import (
    Reaction,
    ReactionCount,
    ReactionType,
    ReactionTypeCustomEmoji,
    ReactionTypeEmoji,
    ReactionTypePaid,
)
from .screenshot_taken import ScreenshotTaken
from .sticker import Sticker
from .stickerset import StickerSet
from .stories_privacy_rules import StoriesPrivacyRules
from .story import Story
from .story_deleted import StoryDeleted
from .story_forward_header import StoryForwardHeader
from .story_skipped import StorySkipped
from .story_views import StoryViews
from .stripped_thumbnail import StrippedThumbnail
from .thumbnail import Thumbnail
from .translated_text import TranslatedText
from .venue import Venue
from .video import Video
from .video_note import VideoNote
from .voice import Voice
from .web_app_data import WebAppData
from .web_page import WebPage
from .web_page_empty import WebPageEmpty
from .web_page_preview import WebPagePreview

__all__ = [
    "Animation",
    "Audio",
    "AvailableEffect",
    "Contact",
    "ContactRegistered",
    "Document",
    "Game",
    "GiftedPremium",
    "Giveaway",
    "GiveawayLaunched",
    "GiveawayResult",
    "LabeledPrice",
    "Location",
    "MediaArea",
    "MediaAreaChannelPost",
    "MediaAreaCoordinates",
    "Message",
    "MessageEntity",
    "Photo",
    "Thumbnail",
    "StrippedThumbnail",
    "Poll",
    "PollOption",
    "PaymentForm",
    "Sticker",
    "StickerSet",
    "Venue",
    "Video",
    "VideoNote",
    "Voice",
    "WebPage",
    "WebPageEmpty",
    "WebPagePreview",
    "Dice",
    "WebAppData",
    "MessageReactions",
    "MessageReactionUpdated",
    "MessageReactionCountUpdated",
    "MessageStory",
    "Story",
    "StoryDeleted",
    "StorySkipped",
    "StoryViews",
    "StoryForwardHeader",
    "Reaction",
    "ReactionType",
    "ReactionTypeEmoji",
    "ReactionTypeCustomEmoji",
    "ReactionTypePaid",
    "ReactionCount",
    "TranslatedText",
    "StoriesPrivacyRules",
    "ExportedStoryLink",
    "ScreenshotTaken",
]
