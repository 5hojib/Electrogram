from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import raw, utils
from pyrogram import types


class RestrictChatMember:
    async def restrict_chat_member(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: datetime = utils.zero_datetime()
    ) -> "types.Chat":
        r = await self.invoke(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=utils.datetime_to_timestamp(until_date),
                    send_messages=not permissions.can_send_messages,
                    send_media=not permissions.can_send_media_messages,
                    embed_links=not permissions.can_add_web_page_previews,
                    send_polls=not permissions.can_send_polls,
                    change_info=not permissions.can_change_info,
                    invite_users=not permissions.can_invite_users,
                    pin_messages=not permissions.can_pin_messages,
                    manage_topics=not permissions.can_manage_topics,
                    send_audios=not permissions.can_send_audios,
                    send_docs=not permissions.can_send_docs,
                    send_games=not permissions.can_send_games,
                    send_gifs=not permissions.can_send_gifs,
                    send_inline=not permissions.can_send_inline,
                    send_photos=not permissions.can_send_photos,
                    send_plain=not permissions.can_send_plain,
                    send_roundvideos=not permissions.can_send_roundvideos,
                    send_stickers=not permissions.can_send_stickers,
                    send_videos=not permissions.can_send_videos,
                    send_voices=not permissions.can_send_voices
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])
