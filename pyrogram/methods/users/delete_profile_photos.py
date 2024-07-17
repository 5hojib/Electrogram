from typing import List, Union

import pyrogram
from pyrogram import raw
from pyrogram import utils
from pyrogram.file_id import FileType


class DeleteProfilePhotos:
    async def delete_profile_photos(
        self: "pyrogram.Client", photo_ids: Union[str, List[str]]
    ) -> bool:
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = [
            utils.get_input_media_from_file_id(i, FileType.PHOTO).id for i in photo_ids
        ]

        return bool(
            await self.invoke(raw.functions.photos.DeletePhotos(id=input_photos))
        )
