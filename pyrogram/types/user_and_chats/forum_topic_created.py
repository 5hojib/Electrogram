from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class ForumTopicCreated(Object):
    """A service message about a new forum topic created in the chat.


    Parameters:
        id (``Integer``):
            Id of the topic

        title (``String``):
            Name of the topic.

        icon_color (``Integer``):
            Color of the topic icon in RGB format

        icon_emoji_id (``Integer``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon
    """

    def __init__(
        self,
        *,
        id: int,
        title: str,
        icon_color: int,
        icon_emoji_id: int | None = None,
    ) -> None:
        super().__init__()

        self.id = id
        self.title = title
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id

    @staticmethod
    def _parse(message: raw.base.Message) -> ForumTopicCreated:
        return ForumTopicCreated(
            id=getattr(message, "id", None),
            title=getattr(message.action, "title", None),
            icon_color=getattr(message.action, "icon_color", None),
            icon_emoji_id=getattr(message.action, "icon_emoji_id", None),
        )
