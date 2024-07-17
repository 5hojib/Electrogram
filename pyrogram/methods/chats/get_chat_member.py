from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.errors import UserNotParticipant


class GetChatMember:
    async def get_chat_member(
        self: "pyrogram.Client", chat_id: Union[int, str], user_id: Union[int, str]
    ) -> "types.ChatMember":
        chat = await self.resolve_peer(chat_id)
        user = await self.resolve_peer(user_id)

        if isinstance(chat, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.GetFullChat(chat_id=chat.chat_id)
            )

            members = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for member in members:
                member = types.ChatMember._parse(self, member, users, {})

                if isinstance(user, raw.types.InputPeerSelf):
                    if member.user.is_self:
                        return member
                else:
                    if member.user.id == user.user_id:
                        return member
            else:
                raise UserNotParticipant
        elif isinstance(chat, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetParticipant(channel=chat, participant=user)
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            return types.ChatMember._parse(self, r.participant, users, chats)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
