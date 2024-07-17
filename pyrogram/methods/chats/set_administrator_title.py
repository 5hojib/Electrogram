from typing import Union

import pyrogram
from pyrogram import raw


class SetAdministratorTitle:
    async def set_administrator_title(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        title: str,
    ) -> bool:
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        r = (
            await self.invoke(
                raw.functions.channels.GetParticipant(
                    channel=chat_id, participant=user_id
                )
            )
        ).participant

        if isinstance(r, raw.types.ChannelParticipantCreator):
            admin_rights = raw.types.ChatAdminRights()
        elif isinstance(r, raw.types.ChannelParticipantAdmin):
            admin_rights = r.admin_rights
        else:
            raise ValueError(
                "Custom titles can only be applied to owners or administrators of supergroups"
            )

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id, user_id=user_id, admin_rights=admin_rights, rank=title
            )
        )

        return True
