from pyrogram import raw
from ..object import Object


class ExportedStoryLink(Object):
    """Contains information about a story viewers.


    Parameters:
        link (``str``):
            The link of the story.
    """

    def __init__(self, *, link: str):
        super().__init__()

        self.link = link

    @staticmethod
    def _parse(exportedstorylink: "raw.types.ExportedStoryLink") -> "ExportedStoryLink":
        return ExportedStoryLink(link=getattr(exportedstorylink, "link", None))
