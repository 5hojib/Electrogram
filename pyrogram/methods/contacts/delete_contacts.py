from typing import List, Union

import pyrogram
from pyrogram import raw, types


class DeleteContacts:
    async def delete_contacts(
        self: "pyrogram.Client",
        user_ids: Union[int, str, List[Union[int, str]]]
    ) -> Union["types.User", List["types.User"], None]:
        is_list = isinstance(user_ids, list)

        if not is_list:
            user_ids = [user_ids]

        r = await self.invoke(
            raw.functions.contacts.DeleteContacts(
                id=[await self.resolve_peer(i) for i in user_ids]
            )
        )

        if not r.updates:
            return None

        users = types.List([types.User._parse(self, i) for i in r.users])

        return users if is_list else users[0]
