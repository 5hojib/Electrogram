from __future__ import annotations

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class Venue(Object):
    """A venue.

    Parameters:
        location (:obj:`~pyrogram.types.Location`):
            Venue location.

        title (``str``):
            Name of the venue.

        address (``str``):
            Address of the venue.

        foursquare_id (``str``, *optional*):
            Foursquare identifier of the venue.

        foursquare_type (``str``, *optional*):
            Foursquare type of the venue.
            (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".)

    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        location: types.Location,
        title: str,
        address: str,
        foursquare_id: str | None = None,
        foursquare_type: str | None = None,
    ) -> None:
        super().__init__(client)

        self.location = location
        self.title = title
        self.address = address
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type

    @staticmethod
    def _parse(client, venue: raw.types.MessageMediaVenue):
        return Venue(
            location=types.Location._parse(client, venue.geo),
            title=venue.title,
            address=venue.address,
            foursquare_id=venue.venue_id or None,
            foursquare_type=venue.venue_type,
            client=client,
        )
