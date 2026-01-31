from __future__ import annotations

from .block_user import BlockUser
from .delete_account import DeleteAccount
from .delete_profile_photos import DeleteProfilePhotos
from .delete_stories import DeleteStories
from .edit_story import EditStory
from .export_story_link import ExportStoryLink
from .forward_story import ForwardStory
from .get_all_stories import GetAllStories
from .get_chat_photos import GetChatPhotos
from .get_chat_photos_count import GetChatPhotosCount
from .get_common_chats import GetCommonChats
from .get_default_emoji_statuses import GetDefaultEmojiStatuses
from .get_me import GetMe
from .get_peer_stories import GetPeerStories
from .get_stories import GetStories
from .get_stories_history import GetUserStoriesHistory
from .get_users import GetUsers
from .send_story import SendStory
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_birthday import UpdateBirthday
from .update_personal_chat import UpdatePersonalChat
from .update_profile import UpdateProfile


class Users(
    BlockUser,
    DeleteStories,
    DeleteAccount,
    EditStory,
    ExportStoryLink,
    ForwardStory,
    GetCommonChats,
    GetChatPhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    GetUsers,
    GetMe,
    GetAllStories,
    GetStories,
    GetUserStoriesHistory,
    GetPeerStories,
    SetUsername,
    GetChatPhotosCount,
    UnblockUser,
    UpdateBirthday,
    UpdatePersonalChat,
    UpdateProfile,
    GetDefaultEmojiStatuses,
    SetEmojiStatus,
    SendStory,
):
    pass
