from ..object import Object


class ScreenshotTaken(Object):
    """A service message that a screenshot of a message in the chat has been taken.
    Currently holds no information.
    """

    def __init__(self):
        super().__init__()