from typing import Union

import pyrogram
from pyrogram import raw, types, errors


class PromoteChatMember:
    async def promote_chat_member(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None,
    ) -> bool:
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        if privileges is None:
            privileges = types.ChatPrivileges()

        try:
            raw_chat_member = (
                await self.invoke(
                    raw.functions.channels.GetParticipant(
                        channel=chat_id, participant=user_id
                    )
                )
            ).participant
        except errors.RPCError:
            raw_chat_member = None

        rank = None
        if isinstance(raw_chat_member, raw.types.ChannelParticipantAdmin):
            rank = raw_chat_member.rank

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                user_id=user_id,
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=privileges.is_anonymous,
                    change_info=privileges.can_change_info,
                    post_messages=privileges.can_post_messages,
                    edit_messages=privileges.can_edit_messages,
                    delete_messages=privileges.can_delete_messages,
                    ban_users=privileges.can_restrict_members,
                    invite_users=privileges.can_invite_users,
                    pin_messages=privileges.can_pin_messages,
                    add_admins=privileges.can_promote_members,
                    manage_call=privileges.can_manage_video_chats,
                    manage_topics=privileges.can_manage_topics,
                    post_stories=privileges.can_post_stories,
                    edit_stories=privileges.can_edit_stories,
                    delete_stories=privileges.can_delete_stories,
                    other=privileges.can_manage_chat,
                ),
                rank=rank or "",
            )
        )

        return True
