from typing import List

import pyrogram
from pyrogram import raw, types

from ..object import Object
from .message import Str


class TranslatedText(Object):
    """A translated text with entities.

    Parameters:
        text (``str``):
            Translated text.

        entities (List of :obj:`~pyrogram.types.MessageEntity`, *optional*):
            Entities of the text.
    """

    def __init__(
        self,
        *,
        text: str,
        entities: List["types.MessageEntity"] = None
    ):
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(
        client,
        translate_result: "raw.types.TextWithEntities"
    ) -> "TranslatedText":
        entities = [
            types.MessageEntity._parse(client, entity, {})
            for entity in translate_result.entities
        ]
        entities = types.List(filter(lambda x: x is not None, entities))

        return TranslatedText(
            text=Str(translate_result.text).init(entities) or None, entities=entities or None
        )
