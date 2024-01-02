import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class Game(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        title: str,
        short_name: str,
        description: str,
        photo: "types.Photo",
        animation: "types.Animation" = None
    ):
        super().__init__(client)

        self.id = id
        self.title = title
        self.short_name = short_name
        self.description = description
        self.photo = photo
        self.animation = animation

    @staticmethod
    def _parse(client, message: "raw.types.Message") -> "Game":
        game: "raw.types.Game" = message.media.game
        animation = None

        if game.document:
            attributes = {type(i): i for i in game.document.attributes}

            file_name = getattr(
                attributes.get(
                    raw.types.DocumentAttributeFilename, None
                ), "file_name", None
            )

            animation = types.Animation._parse(
                client,
                game.document,
                attributes.get(raw.types.DocumentAttributeVideo, None),
                file_name
            )

        return Game(
            id=game.id,
            title=game.title,
            short_name=game.short_name,
            description=game.description,
            photo=types.Photo._parse(client, game.photo),
            animation=animation,
            client=client
        )
