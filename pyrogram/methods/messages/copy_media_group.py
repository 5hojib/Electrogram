from datetime import datetime
from typing import Union, List

import pyrogram
from pyrogram import types, utils, raw


class CopyMediaGroup:
    async def copy_media_group(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        from_chat_id: Union[int, str],
        message_id: int,
        captions: Union[List[str], str] = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
    ) -> List["types.Message"]:
        media_group = await self.get_media_group(from_chat_id, message_id)
        multi_media = []

        reply_to = None
        if reply_to_message_id or message_thread_id:
            reply_to = types.InputReplyToMessage(reply_to_message_id=reply_to_message_id, message_thread_id=message_thread_id)

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
                        captions[i] if isinstance(captions, list) and i < len(captions) and captions[i] else
                        captions if isinstance(captions, str) and i == 0 else
                        message.caption if message.caption and message.caption != "None" and not type(
                            captions) is str else "")
                )
            )

        r = await self.invoke(
            raw.functions.messages.SendMultiMedia(
                peer=await self.resolve_peer(chat_id),
                multi_media=multi_media,
                silent=disable_notification or None,
                reply_to=reply_to,
                noforwards=protect_content,
                schedule_date=utils.datetime_to_timestamp(schedule_date)              
            ),
            sleep_threshold=60
        )

        return await utils.parse_messages(
            self,
            raw.types.messages.Messages(
                messages=[m.message for m in filter(
                  lambda u: isinstance(
                    u, (
                      raw.types.UpdateNewMessage,
                      raw.types.UpdateNewChannelMessage,
                      raw.types.UpdateNewScheduledMessage
                      )
                    ),
                  r.updates
                )],
                users=r.users,
                chats=r.chats
            )
        )
