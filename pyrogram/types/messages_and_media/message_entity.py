from typing import Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from ..object import Object


class MessageEntity(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: "enums.MessageEntityType",
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None,
        language: str = None,
        custom_emoji_id: int = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language
        self.custom_emoji_id = custom_emoji_id

    @staticmethod
    def _parse(client, entity: "raw.base.MessageEntity", users: dict) -> Optional["MessageEntity"]:
        if isinstance(entity, raw.types.InputMessageEntityMentionName):
            entity_type = enums.MessageEntityType.TEXT_MENTION
            user_id = entity.user_id.user_id
        else:
            entity_type = enums.MessageEntityType(entity.__class__)
            user_id = getattr(entity, "user_id", None)

        return MessageEntity(
            type=entity_type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(user_id, None)),
            language=getattr(entity, "language", None),
            custom_emoji_id=getattr(entity, "document_id", None),
            client=client
        )

    async def write(self):
        args = self.__dict__.copy()

        for arg in ("_client", "type", "user"):
            args.pop(arg)

        if self.user:
            args["user_id"] = await self._client.resolve_peer(self.user.id)

        if not self.url:
            args.pop("url")

        if self.language is None:
            args.pop("language")

        args.pop("custom_emoji_id")
        if self.custom_emoji_id is not None:
            args["document_id"] = self.custom_emoji_id

        entity = self.type.value

        if entity is raw.types.MessageEntityMentionName:
            entity = raw.types.InputMessageEntityMentionName

        return entity(**args)
