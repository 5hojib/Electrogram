import pyrogram

from ..object import Object


class InputMessageContent(Object):
    def __init__(self):
        super().__init__()

    async def write(self, client: "pyrogram.Client", reply_markup):
        raise NotImplementedError
