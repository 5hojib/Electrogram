import pyrogram
from pyrogram import raw
from pyrogram.types.object import Object


class Reaction(Object):
    """Contains information about a reaction.

    Parameters:
        emoji (``str``, *optional*):
            Reaction emoji.

        custom_emoji_id (``int``, *optional*):
            Custom emoji id.

        count (``int``, *optional*):
            Reaction count.

        chosen_order (``int``, *optional*):
            Chosen reaction order.
            Available for chosen reactions.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        emoji: str | None = None,
        custom_emoji_id: int | None = None,
        count: int | None = None,
        chosen_order: int | None = None,
    ) -> None:
        super().__init__(client)

        self.emoji = emoji
        self.custom_emoji_id = custom_emoji_id
        self.count = count
        self.chosen_order = chosen_order

    @staticmethod
    def _parse(
        client: "pyrogram.Client", reaction: "raw.base.Reaction"
    ) -> "Reaction":
        if isinstance(reaction, raw.types.ReactionEmoji):
            return Reaction(client=client, emoji=reaction.emoticon)

        if isinstance(reaction, raw.types.ReactionCustomEmoji):
            return Reaction(
                client=client, custom_emoji_id=reaction.document_id
            )
        return None

    @staticmethod
    def _parse_count(
        client: "pyrogram.Client",
        reaction_count: "raw.base.ReactionCount",
    ) -> "Reaction":
        reaction = Reaction._parse(client, reaction_count.reaction)
        reaction.count = reaction_count.count
        reaction.chosen_order = reaction_count.chosen_order

        return reaction
