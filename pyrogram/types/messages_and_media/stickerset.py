from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class StickerSet(Object):
    """A stickerset.

    Parameters:
        id (``Integer``):
            Identifier for this stickerset.

        title (``String``):
            Title of stickerset.

        short_name (``String``):
            Short name of stickerset, used when sharing stickerset using stickerset deep links.

        count (``Integer``):
            Number of stickers in stickerset.

        masks (``Boolean``):
            Is this a mask stickerset.

        animated (``Boolean``):
            Is this a animated stickerset.

        videos (``Boolean``):
            Is this a videos stickerset.

        emojis (``Boolean``):
            Is this a emojis stickerset.
    """

    def __init__(
        self,
        *,
        id: int,
        title: str,
        short_name: str,
        count: int,
        masks: bool | None = None,
        animated: bool | None = None,
        videos: bool | None = None,
        emojis: bool | None = None,
    ) -> None:
        self.id = id
        self.title = title
        self.short_name = short_name
        self.count = count
        self.masks = masks
        self.animated = animated
        self.videos = videos
        self.emojis = emojis

    @staticmethod
    def _parse(stickerset: "raw.types.StickerSet") -> "StickerSet":
        return StickerSet(
            id=getattr(stickerset, "id", None),
            title=getattr(stickerset, "title", None),
            short_name=getattr(stickerset, "short_name", None),
            count=getattr(stickerset, "count", None),
            masks=getattr(stickerset, "masks", None),
            animated=getattr(stickerset, "animated", None),
            videos=getattr(stickerset, "videos", None),
            emojis=getattr(stickerset, "emojis", None),
        )
