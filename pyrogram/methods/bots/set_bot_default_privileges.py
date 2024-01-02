import pyrogram
from pyrogram import raw
from pyrogram import types


class SetBotDefaultPrivileges:
    async def set_bot_default_privileges(
        self: "pyrogram.Client",
        privileges: "types.ChatPrivileges" = None,
        for_channels: bool = None
    ) -> bool:
        function = (
            raw.functions.bots.SetBotBroadcastDefaultAdminRights
            if for_channels
            else raw.functions.bots.SetBotGroupDefaultAdminRights
        )

        admin_rights = raw.types.ChatAdminRights(
            change_info=privileges.can_change_info,
            post_messages=privileges.can_post_messages,
            edit_messages=privileges.can_edit_messages,
            delete_messages=privileges.can_delete_messages,
            ban_users=privileges.can_restrict_members,
            invite_users=privileges.can_invite_users,
            pin_messages=privileges.can_pin_messages,
            add_admins=privileges.can_promote_members,
            anonymous=privileges.is_anonymous,
            manage_call=privileges.can_manage_video_chats,
            other=privileges.can_manage_chat
        ) if privileges else raw.types.ChatAdminRights()

        return await self.invoke(function(admin_rights=admin_rights))
