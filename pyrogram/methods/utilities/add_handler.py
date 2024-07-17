import pyrogram
from pyrogram.handlers import DisconnectHandler
from pyrogram.handlers.handler import Handler


class AddHandler:
    def add_handler(self: "pyrogram.Client", handler: "Handler", group: int = 0):
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group
