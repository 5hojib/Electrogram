from __future__ import annotations

import pyrogram
from pyrogram import raw, types


class SetBotDefaultPrivileges:
    async def set_bot_default_privileges(
        self: pyrogram.Client,
        privileges: types.ChatPrivileges = None,
        for_channels: bool | None = None,
    ) -> bool:
        """Change the default privileges requested by the bot when it's added as an administrator to groups or channels.

        These privileges will be suggested to users, but they are are free to modify the list before adding the bot.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            privileges (:obj:`~pyrogram.types.ChatPrivileges`):
                New default privileges. None to clear.
                Defaults to None.

            for_channels (``bool``, *optional*):
                Pass True to change the default privileges of the bot in channels. Otherwise, the default privileges of
                the bot for groups and supergroups will be changed.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import ChatPrivileges

                await app.set_bot_default_privileges(
                    ChatPrivileges(
                        can_delete_messages=True,
                        can_restrict_members=True
                    )
                )
        """

        function = (
            raw.functions.bots.SetBotBroadcastDefaultAdminRights
            if for_channels
            else raw.functions.bots.SetBotGroupDefaultAdminRights
        )

        admin_rights = (
            raw.types.ChatAdminRights(
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
                other=privileges.can_manage_chat,
            )
            if privileges
            else raw.types.ChatAdminRights()
        )

        return await self.invoke(function(admin_rights=admin_rights))
