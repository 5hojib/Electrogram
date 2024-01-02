from typing import Union, BinaryIO

import pyrogram
from pyrogram import raw


class SetProfilePhoto:
    async def set_profile_photo(
        self: "pyrogram.Client",
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None
    ) -> bool:
        return bool(
            await self.invoke(
                raw.functions.photos.UploadProfilePhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video)
                )
            )
        )
