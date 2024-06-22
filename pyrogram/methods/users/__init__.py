from .block_user import BlockUser
from .delete_profile_photos import DeleteProfilePhotos
from .get_chat_photos import GetChatPhotos
from .get_chat_photos_count import GetChatPhotosCount
from .get_common_chats import GetCommonChats
from .get_default_emoji_statuses import GetDefaultEmojiStatuses
from .get_me import GetMe
from .get_users import GetUsers
from .set_emoji_status import SetEmojiStatus
from .set_profile_photo import SetProfilePhoto
from .set_username import SetUsername
from .unblock_user import UnblockUser
from .update_birthday import UpdateBirthday
from .update_personal_chat import UpdatePersonalChat
from .update_profile import UpdateProfile


class Users(
    BlockUser,
    GetCommonChats,
    GetChatPhotos,
    SetProfilePhoto,
    DeleteProfilePhotos,
    GetUsers,
    GetMe,
    SetUsername,
    GetChatPhotosCount,
    UnblockUser,
    UpdateBirthday,
    UpdatePersonalChat,
    UpdateProfile,
    GetDefaultEmojiStatuses,
    SetEmojiStatus,
):
    pass
