import logging
import re
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import utils
from pyrogram.errors import PeerIdInvalid

log = logging.getLogger(__name__)


class ResolvePeer:
    async def resolve_peer(
        self: "pyrogram.Client", peer_id: Union[int, str]
    ) -> Union[raw.base.InputPeer, raw.base.InputUser, raw.base.InputChannel]:
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return await self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if isinstance(peer_id, str):
                if peer_id in ("self", "me"):
                    return raw.types.InputPeerSelf()

                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())
                peer_id = re.sub(r"https://t.me/", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return await self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        await self.invoke(
                            raw.functions.contacts.ResolveUsername(username=peer_id)
                        )

                        return await self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return await self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                await self.fetch_peers(
                    await self.invoke(
                        raw.functions.users.GetUsers(
                            id=[raw.types.InputUser(user_id=peer_id, access_hash=0)]
                        )
                    )
                )
            elif peer_type == "chat":
                await self.invoke(raw.functions.messages.GetChats(id=[-peer_id]))
            else:
                await self.invoke(
                    raw.functions.channels.GetChannels(
                        id=[
                            raw.types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id), access_hash=0
                            )
                        ]
                    )
                )

            try:
                return await self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid
