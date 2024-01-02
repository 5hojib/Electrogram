from ..object import Object


class RequestPeerTypeChannel(Object):
    def __init__(
        self,
        is_creator: bool=None,
        is_username: bool=None
    ):
        super().__init__()

        self.is_creator = is_creator
        self.is_username = is_username
