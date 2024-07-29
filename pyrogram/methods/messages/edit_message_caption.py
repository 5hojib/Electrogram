from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import enums, types


class EditMessageCaption:
    async def edit_message_caption(
        self: pyrogram.Client,
        chat_id: int | str,
        message_id: int,
        caption: str,
        parse_mode: enums.ParseMode | None = None,
        caption_entities: list[types.MessageEntity] | None = None,
        invert_media: bool = False,
        reply_markup: types.InlineKeyboardMarkup = None,
        business_connection_id: str | None = None,
    ) -> types.Message:
        """Edit the caption of media messages.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                You can also use chat public link in form of *t.me/<username>* (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            caption (``str``):
                New caption of the media message.

            parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
                By default, texts are parsed using both Markdown and HTML styles.
                You can combine both syntaxes together.

            caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
                List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

            invert_media (``bool``, *optional*):
                Inverts the position of the media and caption.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            business_connection_id (``str``, *optional*):
                Unique identifier of the business connection.
                for business bots only.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the edited message is returned.

        Example:
            .. code-block:: python

                await app.edit_message_caption(chat_id, message_id, "new media caption")
        """
        return await self.edit_message_text(
            chat_id=chat_id,
            message_id=message_id,
            text=caption,
            parse_mode=parse_mode,
            entities=caption_entities,
            invert_media=invert_media,
            reply_markup=reply_markup,
            business_connection_id=business_connection_id,
        )
