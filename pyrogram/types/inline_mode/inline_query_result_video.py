from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils, enums
from .inline_query_result import InlineQueryResult


class InlineQueryResultVideo(InlineQueryResult):
    def __init__(
        self,
        video_url: str,
        thumb_url: str,
        title: str,
        id: str = None,
        mime_type: str = "video/mp4",
        video_width: int = 0,
        video_height: int = 0,
        video_duration: int = 0,
        description: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("video", id, input_message_content, reply_markup)

        self.video_url = video_url
        self.thumb_url = thumb_url
        self.title = title
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.mime_type = mime_type

    async def write(self, client: "pyrogram.Client"):
        video = raw.types.InputWebDocument(
            url=self.video_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[raw.types.DocumentAttributeVideo(
                duration=self.video_duration,
                w=self.video_width,
                h=self.video_height
            )]
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[]
        )

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=video,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )
