from __future__ import annotations

from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class WebAppData(Object):
    """Contains data sent from a `Web App <https://core.telegram.org/bots/webapps>`_ to the bot.

    Parameters:
        data (``str``):
            The data.

        button_text (``str``):
            Text of the *web_app* keyboard button, from which the Web App was opened.

    """

    def __init__(
        self,
        *,
        data: str,
        button_text: str,
    ) -> None:
        super().__init__()

        self.data = data
        self.button_text = button_text

    @staticmethod
    def _parse(action: raw.types.MessageActionWebViewDataSentMe):
        return WebAppData(data=action.data, button_text=action.text)
