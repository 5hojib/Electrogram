from __future__ import annotations

from typing import TYPE_CHECKING

from .handler import Handler

if TYPE_CHECKING:
    from collections.abc import Callable


class StoryHandler(Handler):
    """The Story handler class. Used to handle new stories.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_story` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Stories arrives. It takes *(client, story)*
            as positional arguments (look at the section below for a detailed description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of stories to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the story handler.

        story (:obj:`~pyrogram.types.Story`):
            The received story.
    """

    def __init__(self, callback: Callable, filters=None) -> None:
        super().__init__(callback, filters)
