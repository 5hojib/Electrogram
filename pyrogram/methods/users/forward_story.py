from typing import List, Union

import pyrogram
from pyrogram import enums, types

class ForwardStory:
    def _split(self, message, entities, *args, **kwargs):
        return message, entities

    async def forward_story(
        self: "pyrogram.Client",
        from_chat_id: Union[int, str],
        from_story_id: int,
        chat_id: int = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        pinned: bool = None,
        protect_content: bool = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        period: int = None
    ) -> "types.Story":
        return await self.send_story(
            chat_id=chat_id,
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users,
            pinned=pinned,
            protect_content=protect_content,
            caption=caption,
            caption_entities=caption_entities,
            parse_mode=parse_mode,
            period=period,
            forward_from_chat_id=from_chat_id,
            forward_from_story_id=from_story_id
        )
