from __future__ import annotations

import pyrogram
from pyrogram import raw, types

from .menu_button import MenuButton


class MenuButtonWebApp(MenuButton):
    """A menu button, which launches a `Web App <https://core.telegram.org/bots/webapps>`_.

    Parameters:
        text (``str``):
            Text on the button

        web_app (:obj:`~pyrogram.types.WebAppInfo`):
            Description of the Web App that will be launched when the user presses the button.
            The Web App will be able to send an arbitrary message on behalf of the user using the method
            :meth:`~pyrogram.Client.answer_web_app_query`.
    """

    def __init__(self, text: str, web_app: types.WebAppInfo) -> None:
        super().__init__("web_app")

        self.text = text
        self.web_app = web_app

    async def write(
        self,
        client: pyrogram.Client,  # noqa: ARG002
    ) -> raw.types.BotMenuButton:
        return raw.types.BotMenuButton(text=self.text, url=self.web_app.url)
