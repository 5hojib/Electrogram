from pyrogram import raw
from typing import List
from ..object import Object

class StoryViews(Object):
    """Contains information about a story viewers.


    Parameters:
        view_count (``int``):
            The count of stories viewers.

        recent_viewers (List of ``int``):
            List of user_id of recent stories viewers.
    """

    def __init__(
            self, *,
            view_count: int,
            recent_viewers: List[int] = None
    ):
        super().__init__()

        self.view_count = view_count
        self.recent_viewers = recent_viewers

    @staticmethod
    def _parse(storyviews: "raw.types.StoryViews") -> "StoryViews":
        return StoryViews(
            view_count=getattr(storyviews,"view_count", None),
            recent_viewers=getattr(storyviews,"recent_viewers", None)
        )
