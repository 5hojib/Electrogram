from pyrogram import raw
from ..object import Object


class WebPageEmpty(Object):
    # TODO: hash, cached_page
    """A webpage preview

    Parameters:
        id (``str``):
            Unique identifier for this webpage.

        url (``str``):
            Full URL for this webpage.
    """

    def __init__(self, *, id: str, url: str):
        super().__init__()

        self.id = id
        self.url = url

    @staticmethod
    def _parse(webpage: "raw.types.WebPageEmpty") -> "WebPageEmpty":
        return WebPageEmpty(id=str(webpage.id), url=webpage.url)
