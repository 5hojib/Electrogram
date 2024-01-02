from pyrogram import raw, types
from ..object import Object


class KeyboardButton(Object):
    def __init__(
        self,
        text: str,
        request_contact: bool = None,
        request_location: bool = None,
        request_channel: "types.RequestPeerTypeChannel" = None,
        request_chat: "types.RequestPeerTypeChat" = None,
        request_user: "types.RequestPeerTypeUser" = None,
        web_app: "types.WebAppInfo" = None
    ):
        super().__init__()

        self.text = str(text)
        self.request_contact = request_contact
        self.request_location = request_location
        self.request_channel = request_channel
        self.request_chat = request_chat
        self.request_user = request_user
        self.web_app = web_app

    @staticmethod
    def read(b):
        if isinstance(b, raw.types.KeyboardButton):
            return b.text

        if isinstance(b, raw.types.KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(b, raw.types.KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

        if isinstance(b, raw.types.KeyboardButtonSimpleWebView):
            return KeyboardButton(
                text=b.text,
                web_app=types.WebAppInfo(
                    url=b.url
                )
            )

        if isinstance(b, raw.types.RequestPeerTypeBroadcast):
            return KeyboardButton(
                text=b.text,
                request_chat=types.RequestPeerTypeChannel(
                    is_creator=b.creator,
                    is_username=b.has_username
                )
            )

        if isinstance(b, raw.types.RequestPeerTypeChat):
            return KeyboardButton(
                text=b.text,
                request_chat=types.RequestPeerTypeChat(
                    is_creator=b.creator,
                    is_bot_participant=b.bot_participant,
                    is_username=b.has_username,
                    is_forum=b.forum
                )
            )

        if isinstance(b, raw.types.RequestPeerTypeUser):
            return KeyboardButton(
                text=b.text,
                request_user=types.RequestPeerTypeUser(
                    is_bot=b.bot,
                    is_premium=b.premium
                )
            )

    def write(self):
        if self.request_contact:
            return raw.types.KeyboardButtonRequestPhone(text=self.text)
        elif self.request_location:
            return raw.types.KeyboardButtonRequestGeoLocation(text=self.text)
        elif self.request_channel:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeBroadcast(
                    creator=self.request_broadcast.is_creator,
                    has_username=self.request_broadcast.is_username
                )
            )
        elif self.request_chat:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeChat(
                    creator=self.request_chat.is_creator,
                    bot_participant=self.request_chat.is_bot_participant,
                    has_username=self.request_chat.is_username,
                    forum=self.request_chat.is_forum
                )
            )
        elif self.request_user:
            return raw.types.KeyboardButtonRequestPeer(
                text=self.text,
                button_id=0,
                peer_type=raw.types.RequestPeerTypeUser(
                    bot=self.request_user.is_bot,
                    premium=self.request_user.is_premium
                )
            )
        elif self.web_app:
            return raw.types.KeyboardButtonSimpleWebView(text=self.text, url=self.web_app.url)
        else:
            return raw.types.KeyboardButton(text=self.text)
