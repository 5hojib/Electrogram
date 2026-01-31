from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class ExportedStoryLink(Object):
    """Contains information about a story viewers.


    Parameters:
        link (``str``):
            The link of the story.
    """

    def __init__(self, *, link: str) -> None:
        super().__init__()

        self.link = link

    @staticmethod
    def _parse(
        exportedstorylink: raw.types.ExportedStoryLink,
    ) -> ExportedStoryLink:
        return ExportedStoryLink(link=getattr(exportedstorylink, "link", None))
