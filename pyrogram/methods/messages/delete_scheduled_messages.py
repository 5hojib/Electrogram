from typing import Union, Iterable

import pyrogram
from pyrogram import raw


class DeleteScheduledMessages:
    async def delete_scheduled_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]]
    ) -> int:
        """Delete scheduled messages.
        .. include:: /_includes/usable-by/users-bots.rst
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).
            message_ids (``int`` | Iterable of ``int``):
                An iterable of message identifiers to delete (integers) or a single message id.
        Returns:
            ``int`` | List of ``int``: In case *message_ids* was not
            a list, a single message id is returned, otherwise a list of messages ids is returned.
        Example:
            .. code-block:: python
                # Delete one message
                await app.delete_scheduled_messages(chat_id, message_id)
                # Delete multiple messages at once
                await app.delete_scheduled_messages(chat_id, list_of_message_ids)
        """
        peer = await self.resolve_peer(chat_id)
        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]

        r = await self.invoke(
            raw.functions.channels.DeleteMessages(
                peer=peer,
                id=message_ids
            )
        )

        return r.messages if is_iterable else r.messages[0]