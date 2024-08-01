from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    import pyrogram
    from pyrogram import raw


class Dice(Object):
    """A dice with a random value from 1 to 6 for currently supported base emoji.

    Parameters:
        emoji (``string``):
            Emoji on which the dice throw animation is based.

        value (``int``):
            Value of the dice, 1-6 for currently supported base emoji.
    """

    def __init__(
        self,
        *,
        client: pyrogram.Client = None,
        emoji: str,
        value: int,
    ) -> None:
        super().__init__(client)

        self.emoji = emoji
        self.value = value

    @staticmethod
    def _parse(client, dice: raw.types.MessageMediaDice) -> Dice:
        return Dice(emoji=dice.emoticon, value=dice.value, client=client)
