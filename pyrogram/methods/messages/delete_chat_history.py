from datetime import datetime
import logging
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import utils

log = logging.getLogger(__name__)


class DeleteChatHistory:
    async def delete_chat_history(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        max_id: int = 0,
        revoke: bool = None,
        just_clear: bool = None,
        min_date: datetime = None,
        max_date: datetime = None,
    ) -> int:
        """Delete the history of a chat.
        .. include:: /_includes/usable-by/users.rst
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
            max_id (``int``, *optional*):
                Maximum ID of message to delete.
            revoke (``bool``, *optional*):
                Deletes messages history for everyone.
                Required ``True`` if using in channel.
            just_clear (``bool``, *optional*):
                If True, clear history for the current user, without actually removing chat.
                For private and simple group chats only.
            min_date (:py:obj:`~datetime.datetime`, *optional*):
                Delete all messages newer than this time.
                For private and simple group chats only.
            max_date (:py:obj:`~datetime.datetime`, *optional*):
                Delete all messages older than this time.
                For private and simple group chats only.
        Returns:
            ``int``: Amount of affected messages
        Example:
            .. code-block:: python
                # Delete all messages in channel
                await app.delete_chat_history(chat_id, revoke=True)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.DeleteHistory(
                    channel=raw.types.InputChannel(
                        channel_id=peer.channel_id,
                        access_hash=peer.access_hash
                    ),
                    max_id=max_id,
                    for_everyone=revoke
                )
            )
        else:
            r = await self.invoke(
                raw.functions.messages.DeleteHistory(
                    peer=peer,
                    max_id=max_id,
                    just_clear=just_clear,
                    revoke=revoke,
                    min_date=utils.datetime_to_timestamp(min_date),
                    max_date=utils.datetime_to_timestamp(max_date)
                )
            )

        return len(r.updates[0].messages) if isinstance(peer, raw.types.InputPeerChannel) else r.pts_count