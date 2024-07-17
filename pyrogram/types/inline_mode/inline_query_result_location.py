import pyrogram
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult


class InlineQueryResultLocation(InlineQueryResult):
    def __init__(
        self,
        title: str,
        latitude: float,
        longitude: float,
        horizontal_accuracy: float = None,
        live_period: int = None,
        heading: int = None,
        proximity_alert_radius: int = None,
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0,
    ):
        super().__init__("location", id, input_message_content, reply_markup)

        self.title = title
        self.latitude = latitude
        self.longitude = longitude
        self.horizontal_accuracy = horizontal_accuracy
        self.live_period = live_period
        self.heading = heading
        self.proximity_alert_radius = proximity_alert_radius
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
                else raw.types.InputBotInlineMessageMediaGeo(
                    geo_point=raw.types.InputGeoPoint(
                        lat=self.latitude, long=self.longitude
                    ),
                    heading=self.heading,
                    period=self.live_period,
                    proximity_notification_radius=self.proximity_alert_radius,
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                )
            ),
        )
