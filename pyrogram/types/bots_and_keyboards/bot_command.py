from pyrogram import raw

from ..object import Object


class BotCommand(Object):
    def __init__(self, command: str, description: str):
        super().__init__()

        self.command = command
        self.description = description

    def write(self) -> "raw.types.BotCommand":
        return raw.types.BotCommand(
            command=self.command,
            description=self.description,
        )

    @staticmethod
    def read(c: "raw.types.BotCommand") -> "BotCommand":
        return BotCommand(command=c.command, description=c.description)
