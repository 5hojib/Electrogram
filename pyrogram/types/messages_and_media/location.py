from __future__ import annotations

import pyrogram
from pyrogram import raw
from pyrogram.types.object import Object


class Location(Object):
    """A point on the map.

    Parameters:
        longitude (``float``):
            Longitude as defined by sender.

        latitude (``float``):
            Latitude as defined by sender.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        longitude: float,
        latitude: float,
    ) -> None:
        super().__init__(client)

        self.longitude = longitude
        self.latitude = latitude

    @staticmethod
    def _parse(client, geo_point: raw.types.GeoPoint) -> Location:
        if isinstance(geo_point, raw.types.GeoPoint):
            return Location(
                longitude=geo_point.long,
                latitude=geo_point.lat,
                client=client,
            )
        return None
