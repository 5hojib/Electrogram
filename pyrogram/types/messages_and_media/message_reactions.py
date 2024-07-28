from typing import Optional

import pyrogram
from pyrogram import raw, types
from pyrogram.types.object import Object


class MessageReactions(Object):
    """Contains information about a message reactions.

    Parameters:
        reactions (List of :obj:`~pyrogram.types.Reaction`):
            Reactions list.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        reactions: list["types.Reaction"] | None = None,
    ):
        super().__init__(client)

        self.reactions = reactions

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        message_reactions: Optional[
            "raw.base.MessageReactions"
        ] = None,
    ) -> Optional["MessageReactions"]:
        if not message_reactions:
            return None

        return MessageReactions(
            client=client,
            reactions=[
                types.Reaction._parse_count(client, reaction)
                for reaction in message_reactions.results
            ],
        )
