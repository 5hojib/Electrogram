from typing import Union, List

import pyrogram
from pyrogram import raw


class ArchiveChats:
    async def archive_chats(
        self: "pyrogram.Client",
        chat_ids: Union[int, str, List[Union[int, str]]],
    ) -> bool:
        """Archive one or more chats.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_ids (``int`` | ``str`` | List[``int``, ``str``]):
                Unique identifier (int) or username (str) of the target chat.
                You can also pass a list of ids (int) or usernames (str).
                You can also use chat public link in form of *t.me/<username>* (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Archive chat
                await app.archive_chats(chat_id)

                # Archive multiple chats at once
                await app.archive_chats([chat_id1, chat_id2, chat_id3])
        """

        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = []

        for chat in chat_ids:
            folder_peers.append(
                raw.types.InputFolderPeer(
                    peer=await self.resolve_peer(chat), folder_id=1
                )
            )

        await self.invoke(
            raw.functions.folders.EditPeerFolders(folder_peers=folder_peers)
        )

        return True
