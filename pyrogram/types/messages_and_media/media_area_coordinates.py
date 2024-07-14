from pyrogram import raw
from ..object import Object


class MediaAreaCoordinates(Object):
    def __init__(
        self,
        x: float = None,
        y: float = None,
        width: float = None,
        height: float = None,
        rotation: float = None
    ):
        super().__init__()

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rotation = rotation

    def _parse(
            media_area_cordinates: "raw.types.MediaAreaCoordinates"
    ) -> "MediaAreaCoordinates":
        return MediaAreaCoordinates(
            x=media_area_cordinates.x,
            y=media_area_cordinates.y,
            width=media_area_cordinates.w,
            height=media_area_cordinates.h,
            rotation=media_area_cordinates.rotation
        )

    def write(self):
        return raw.types.MediaAreaCoordinates(
            x=self.x or 51.596797943115,
            y=self.y or 51.580257415771,
            w=self.width or 69.867012023926,
            h=self.height or 75.783416748047,
            rotation=self.rotation or 0.0
        ).write()
