from __future__ import annotations

from typing import TYPE_CHECKING

from .handler import Handler

if TYPE_CHECKING:
    from collections.abc import Callable


class MessageReactionCountUpdatedHandler(Handler):
    """The MessageReactionCountUpdated handler class.
    Used to handle changes in the anonymous reaction of a message.

    It is intended to be used with :meth:`~pyrogram.Client.add_handler`.

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_message_reaction_count_updated` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new MessageReactionCountUpdated event arrives. It takes
            *(client, message_reaction_count_updated)* as positional arguments (look at the section below for a detailed
            description).

        filters (:obj:`Filters`):
            Pass one or more filters to allow only a subset of updates to be passed in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the handler.

        message_reaction_count_updated (:obj:`~pyrogram.types.MessageReactionCountUpdated`):
            The received message reaction count update.
    """

    def __init__(self, callback: Callable, filters=None) -> None:
        super().__init__(callback, filters)
