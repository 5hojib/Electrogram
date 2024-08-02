from __future__ import annotations

from typing import TYPE_CHECKING

import pyrogram
from pyrogram import raw, types, utils

if TYPE_CHECKING:
    from datetime import datetime


class CopyMediaGroup:
    async def copy_media_group(
        self: pyrogram.Client,
        chat_id: int | str,
        from_chat_id: int | str,
        message_id: int,
        captions: list[str] | str | None = None,
        disable_notification: bool | None = None,
        message_thread_id: int | None = None,
        reply_to_message_id: int | None = None,
        schedule_date: datetime | None = None,
        protect_content: bool | None = None,
    ) -> list[types.Message]:
        """Copy a media group by providing one of the message ids.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            from_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the source chat where the original media group was sent.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Message identifier in the chat specified in *from_chat_id*.

            captions (``str`` | List of ``str`` , *optional*):
                New caption for media, 0-1024 characters after entities parsing for each media.
                If not specified, the original caption is kept.
                Pass "" (empty string) to remove the caption.

                If a ``string`` is passed, it becomes a caption only for the first media.
                If a list of ``string`` passed, each element becomes caption for each media element.
                You can pass ``None`` in list to keep the original caption (see examples below).

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            message_thread_id (``int``, *optional*):
                Unique identifier for the target message thread (topic) of the forum.
                for forum supergroups only.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            schedule_date (:py:obj:`~datetime.datetime`, *optional*):
                Date when the message will be automatically sent.

            protect_content (``bool``, *optional*):
                Protects the contents of the sent message from forwarding and saving

        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of copied messages is returned.

        Example:
            .. code-block:: python

                # Copy a media group
                await app.copy_media_group(to_chat, from_chat, 123)

                await app.copy_media_group(to_chat, from_chat, 123, captions="single caption")

                await app.copy_media_group(to_chat, from_chat, 123,
                    captions=["caption 1", None, ""])
        """

        media_group = await self.get_media_group(from_chat_id, message_id)
        multi_media = []

        reply_to = None
        if reply_to_message_id or message_thread_id:
            reply_to = types.InputReplyToMessage(
                reply_to_message_id=reply_to_message_id,
                message_thread_id=message_thread_id,
            )

        for i, message in enumerate(media_group):
            if message.photo:
                file_id = message.photo.file_id
            elif message.audio:
                file_id = message.audio.file_id
            elif message.document:
                file_id = message.document.file_id
            elif message.video:
                file_id = message.video.file_id
            else:
                raise ValueError("Message with this type can't be copied.")

            media = utils.get_input_media_from_file_id(file_id=file_id)
            multi_media.append(
                raw.types.InputSingleMedia(
                    media=media,
                    random_id=self.rnd_id(),
                    **await self.parser.parse(
                        captions[i]
                        if isinstance(captions, list)
                        and i < len(captions)
                        and captions[i]
                        else captions
                        if isinstance(captions, str) and i == 0
                        else message.caption
                        if message.caption
                        and message.caption != "None"
                        and type(captions) is not str
                        else ""
                    ),
                )
            )

        r = await self.invoke(
            raw.functions.messages.SendMultiMedia(
                peer=await self.resolve_peer(chat_id),
                multi_media=multi_media,
                silent=disable_notification or None,
                reply_to=reply_to,
                noforwards=protect_content,
                schedule_date=utils.datetime_to_timestamp(schedule_date),
            ),
            sleep_threshold=60,
        )

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[
                    m.message
                    for m in filter(
                        lambda u: isinstance(
                            u,
                            raw.types.UpdateNewMessage
                            | raw.types.UpdateNewChannelMessage
                            | raw.types.UpdateNewScheduledMessage,
                        ),
                        r.updates,
                    )
                ],
                users=r.users,
                chats=r.chats,
            ),
        )
