from pyrogram import raw, types
from ..object import Object
from typing import Union


class KeyboardButton(Object):
    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        request_chat: Union[
            "types.RequestPeerTypeChat", "types.RequestPeerTypeChannel"
        ] = None,
        request_user: "types.RequestPeerTypeUser" = None,
        web_app: "types.WebAppInfo" = None,
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_chat = request_chat
        self.request_user = request_user
        self.web_app = web_app

    @staticmethod
    def read(b):
        if isinstance(b, raw.types.KeyboardButton):
            return b.text

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(text=b.text, request_contact=True)

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(text=b.text, request_location=True)

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(text=b.text, web_app=types.WebAppInfo(url=b.url))

        if isinstance(b, raw.types.KeyboardButtonRequestPeer):
            if isinstance(b.peer_type, raw.types.RequestPeerTypeBroadcast):
                return KeyboardButton(
                    text=b.text,
                    request_chat=types.RequestPeerTypeChannel(
                        is_creator=b.peer_type.creator,
                        is_username=b.peer_type.has_username,
                        max=b.max_quantity,
                    ),
                )
            if isinstance(b.peer_type, raw.types.RequestPeerTypeChat):
                return KeyboardButton(
                    text=b.text,
                    request_chat=types.RequestPeerTypeChat(
                        is_creator=b.peer_type.creator,
                        is_bot_participant=b.peer_type.bot_participant,
                        is_username=b.peer_type.has_username,
                        is_forum=b.peer_type.forum,
                        max=b.max_quantity,
                    ),
                )

            if isinstance(b.peer_type, raw.types.RequestPeerTypeUser):
                return KeyboardButton(
                    text=b.text,
                    request_user=types.RequestPeerTypeUser(
                        is_bot=b.peer_type.bot,
                        is_premium=b.peer_type.premium,
                        max=b.max_quantity,
                    ),
                )

    def write(self):
        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text)
        elif self.request_chat:
            if isinstance(self.request_chat, types.RequestPeerTypeChannel):
                return raw.types.KeyboardButtonRequestPeer(
                    text=self.text,
                    button_id=0,
                    peer_type=raw.types.RequestPeerTypeBroadcast(
                        creator=self.request_chat.is_creator,
                        has_username=self.request_chat.is_username,
                    ),
                    max_quantity=self.request_chat.max,
                )
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeChat(
                    creator=self.request_chat.is_creator,
                    bot_participant=self.request_chat.is_bot_participant,
                    has_username=self.request_chat.is_username,
                    forum=self.request_chat.is_forum,
                ),
                max_quantity=self.request_chat.max,
            )
        elif self.request_user:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeUser(
                    bot=self.request_user.is_bot, premium=self.request_user.is_premium
                ),
                max_quantity=self.request_user.max,
            )
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(
                text=self.text, url=self.web_app.url
            )
        else:
            return raw.types.KeyboardButton(text=self.text)
