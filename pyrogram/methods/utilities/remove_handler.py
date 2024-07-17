import pyrogram
from pyrogram.handlers import DisconnectHandler
from pyrogram.handlers.handler import Handler


class RemoveHandler:
    def remove_handler(self: "pyrogram.Client", handler: "Handler", group: int = 0):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)
