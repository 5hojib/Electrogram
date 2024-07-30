from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class TermsOfService(Object):
    """Telegram's Terms of Service returned by :meth:`~pyrogram.Client.sign_in`.

    Parameters:
        id (``str``):
            Terms of Service identifier.

        text (``str``):
            Terms of Service text.

        entities (List of :obj:`~pyrogram.types.MessageEntity`):
            Special entities like URLs that appear in the text.
    """

    def __init__(
        self,
        *,
        id: str,
        text: str,
        entities: list[types.MessageEntity],
    ) -> None:
        super().__init__()

        self.id = id
        self.text = text
        self.entities = entities

    @staticmethod
    def _parse(
        terms_of_service: raw.types.help.TermsOfService,
    ) -> TermsOfService:
        return TermsOfService(
            id=terms_of_service.id.data,
            text=terms_of_service.text,
            entities=[
                types.MessageEntity._parse(None, entity, {})
                for entity in terms_of_service.entities
            ]
            if terms_of_service.entities
            else None,
        )
