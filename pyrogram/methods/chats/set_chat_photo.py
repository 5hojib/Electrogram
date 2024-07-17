import os
from typing import Union, BinaryIO

import pyrogram
from pyrogram import raw
from pyrogram import utils
from pyrogram.file_id import FileType


class SetChatPhoto:
    async def set_chat_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        video_start_ts: float = None,
    ) -> bool:
        peer = await self.resolve_peer(chat_id)

        if isinstance(photo, str):
            if os.path.isfile(photo):
                photo = raw.types.InputChatUploadedPhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video),
                    video_start_ts=video_start_ts,
                )
            else:
                photo = utils.get_input_media_from_file_id(photo, FileType.PHOTO)
                photo = raw.types.InputChatPhoto(id=photo.id)
        else:
            photo = raw.types.InputChatUploadedPhoto(
                file=await self.save_file(photo),
                video=await self.save_file(video),
                video_start_ts=video_start_ts,
            )

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id,
                    photo=photo,
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditPhoto(channel=peer, photo=photo)
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True
