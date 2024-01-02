import pyrogram
from pyrogram import raw
from ..object import Object


class Dice(Object):
    def __init__(self, *, client: "pyrogram.Client" = None, emoji: str, value: int):
        super().__init__(client)

        self.emoji = emoji
        self.value = value

    @staticmethod
    def _parse(client, dice: "raw.types.MessageMediaDice") -> "Dice":
        return Dice(
            emoji=dice.emoticon,
            value=dice.value,
            client=client
        )
