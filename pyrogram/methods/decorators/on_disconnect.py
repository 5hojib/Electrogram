from typing import Callable

import pyrogram


class OnDisconnect:
    def on_disconnect(self=None) -> Callable:
        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.handlers.DisconnectHandler(func))
            else:
                if not hasattr(func, "handlers"):
                    func.handlers = []

                func.handlers.append((pyrogram.handlers.DisconnectHandler(func), 0))

            return func

        return decorator
