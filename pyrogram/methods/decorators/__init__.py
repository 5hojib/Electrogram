from __future__ import annotations

from .on_bot_business_connect import OnBotBusinessConnect
from .on_bot_business_message import OnBotBusinessMessage
from .on_callback_query import OnCallbackQuery
from .on_chat_join_request import OnChatJoinRequest
from .on_chat_member_updated import OnChatMemberUpdated
from .on_chosen_inline_result import OnChosenInlineResult
from .on_deleted_bot_business_messages import (
    OnDeletedBotBusinessMessages,
)
from .on_deleted_messages import OnDeletedMessages
from .on_disconnect import OnDisconnect
from .on_edited_bot_business_message import OnEditedBotBusinessMessage
from .on_edited_message import OnEditedMessage
from .on_inline_query import OnInlineQuery
from .on_message import OnMessage
from .on_message_reaction_count_updated import (
    OnMessageReactionCountUpdated,
)
from .on_message_reaction_updated import OnMessageReactionUpdated
from .on_poll import OnPoll
from .on_pre_checkout_query import OnPreCheckoutQuery
from .on_raw_update import OnRawUpdate
from .on_shipping_query import OnShippingQuery
from .on_story import OnStory
from .on_user_status import OnUserStatus


class Decorators(
    OnBotBusinessConnect,
    OnMessage,
    OnBotBusinessMessage,
    OnEditedMessage,
    OnEditedBotBusinessMessage,
    OnDeletedMessages,
    OnDeletedBotBusinessMessages,
    OnCallbackQuery,
    OnShippingQuery,
    OnPreCheckoutQuery,
    OnRawUpdate,
    OnDisconnect,
    OnUserStatus,
    OnInlineQuery,
    OnPoll,
    OnChosenInlineResult,
    OnChatMemberUpdated,
    OnChatJoinRequest,
    OnStory,
    OnMessageReactionUpdated,
    OnMessageReactionCountUpdated,
):
    pass
