import pyrogram
from pyrogram import raw, types
from .inline_query_result import InlineQueryResult


class InlineQueryResultContact(InlineQueryResult):
    def __init__(
        self,
        phone_number: str,
        first_name: str,
        last_name: str = "",
        vcard: str = "",
        id: str = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0,
    ):
        super().__init__("contact", id, input_message_content, reply_markup)

        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.vcard = vcard
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "pyrogram.Client"):
        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.first_name,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaContact(
                    phone_number=self.phone_number,
                    first_name=self.first_name,
                    last_name=self.last_name,
                    vcard=self.vcard,
                    reply_markup=await self.reply_markup.write(client)
                    if self.reply_markup
                    else None,
                )
            ),
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpg",
                attributes=[
                    raw.types.DocumentAttributeImageSize(
                        w=self.thumb_width, h=self.thumb_height
                    )
                ],
            )
            if self.thumb_url
            else None,
        )
