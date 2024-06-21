from .on_callback_query import OnCallbackQuery
from .on_chat_join_request import OnChatJoinRequest
from .on_chat_member_updated import OnChatMemberUpdated
from .on_chosen_inline_result import OnChosenInlineResult
from .on_deleted_messages import OnDeletedMessages
from .on_disconnect import OnDisconnect
from .on_edited_message import OnEditedMessage
from .on_inline_query import OnInlineQuery
from .on_message import OnMessage
from .on_raw_update import OnRawUpdate
from .on_user_status import OnUserStatus
from .on_message_reaction_updated import OnMessageReactionUpdated
from .on_message_reaction_count_updated import OnMessageReactionCountUpdated

class Decorators(
    OnMessage,
    OnEditedMessage,
    OnDeletedMessages,
    OnCallbackQuery,
    OnRawUpdate,
    OnDisconnect,
    OnUserStatus,
    OnInlineQuery,
    OnChosenInlineResult,
    OnChatMemberUpdated,
    OnChatJoinRequest,
    OnMessageReactionUpdated,
    OnMessageReactionCountUpdated
):
    pass
