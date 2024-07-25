from ..object import Object


class RequestPeerTypeUser(Object):
    """Object used to request clients to send a user identifier.

    Parameters:
        is_bot (``bool``, *optional*):
            If True, show only Bots.

        is_premium (``bool``, *optional*):
            If True, show only Premium Users.
    """

    def __init__(self, is_bot: bool = None, is_premium: bool = None, max: int = 1):
        super().__init__()

        self.is_bot = is_bot
        self.is_premium = is_premium
        self.max = max
