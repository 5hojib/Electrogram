import pyrogram
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult


class InlineQueryResultVenue(InlineQueryResult):
    def __init__(
        self,
        title: str,
        address: str,
        latitude: float,
        longitude: float,
        id: str = None,
        foursquare_id: str = None,
        foursquare_type: str = None,
        google_place_id: str = None,
        google_place_type: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("venue", id, input_message_content, reply_markup)

        self.title = title
        self.address = address
        self.latitude = latitude
        self.longitude = longitude
        self.foursquare_id = foursquare_id
        self.foursquare_type = foursquare_type
        self.google_place_id = google_place_id
        self.google_place_type = google_place_type
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaVenue(
                    geo_point=raw.types.InputGeoPoint(
                        lat=self.latitude,
                        long=self.longitude
                    ),
                    title=self.title,
                    address=self.address,
                    provider=(
                        "foursquare" if self.foursquare_id or self.foursquare_type
                        else "google" if self.google_place_id or self.google_place_type
                        else ""
                    ),
                    venue_id=self.foursquare_id or self.google_place_id or "",
                    venue_type=self.foursquare_type or self.google_place_type or "",
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None
                )
            )
        )
