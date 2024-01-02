from ..object import Object


class RequestPeerTypeUser(Object):
    def __init__(
        self,
        is_bot: bool=None,
        is_premium: bool=None,
        max: int=1
    ):
        super().__init__()

        self.is_bot = is_bot
        self.is_premium = is_premium
        self.max = max
