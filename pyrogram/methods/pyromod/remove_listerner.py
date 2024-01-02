import pyrogram
from pyrogram.types import Listener

class RemoveListener:
    def remove_listener(
        self: "pyrogram.Client",
        listener: Listener
    ):
        try:
            self.listeners[listener.listener_type].remove(listener)
        except ValueError:
            pass
