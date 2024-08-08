from __future__ import annotations

import pyrogram
from pyrogram import raw, types, utils
from pyrogram.types.object import Object


class FoundContacts(Object):
    """Chats found by name substring and auxiliary data.
    Parameters:
        my_results (List of :obj:`~pyrogram.types.Chat`, *optional*):
            Personalized results.
        global_results (List of :obj:`~pyrogram.types.Chat`, *optional*):
            List of found chats in global search.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        my_results: types.Chat | None = None,
        global_results: types.Chat | None = None,
    ) -> None:
        super().__init__(client)

        self.my_results = my_results
        self.global_results = global_results

    @staticmethod
    def _parse(client, found: raw.types.contacts.Found) -> FoundContacts:
        users = {u.id: u for u in found.users}
        chats = {c.id: c for c in found.chats}

        my_results = []
        global_results = []

        for result in found.my_results:
            peer_id = utils.get_raw_peer_id(result)
            peer = users.get(peer_id) or chats.get(peer_id)

            my_results.append(types.Chat._parse_chat(client, peer))

        for result in found.results:
            peer_id = utils.get_raw_peer_id(result)
            peer = users.get(peer_id) or chats.get(peer_id)

            global_results.append(types.Chat._parse_chat(client, peer))

        return FoundContacts(
            my_results=types.List(my_results) or None,
            global_results=types.List(global_results) or None,
            client=client,
        )
