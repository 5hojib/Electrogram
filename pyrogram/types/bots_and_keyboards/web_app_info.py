from __future__ import annotations

from pyrogram.types.object import Object


class WebAppInfo(Object):
    """Contains information about a `Web App <https://core.telegram.org/bots/webapps>`_.

    Parameters:
        url (``str``):
            An HTTPS URL of a Web App to be opened with additional data as specified in
            `Initializing Web Apps <https://core.telegram.org/bots/webapps#initializing-web-apps>`_.
    """

    def __init__(
        self,
        *,
        url: str,
    ) -> None:
        super().__init__()

        self.url = url
