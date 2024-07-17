from typing import Callable

import pyrogram
from pyrogram.filters import Filter


class OnChatMemberUpdated:
    def on_chat_member_updated(self=None, filters=None, group: int = 0) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(
                    pyrogram.handlers.ChatMemberUpdatedHandler(func, filters), group
                )
            elif isinstance(self, Filter) or self is None:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append(
                    (
                        pyrogram.handlers.ChatMemberUpdatedHandler(func, self),
                        group if filters is None else filters,
                    )
                )

            return func

        return decorator
