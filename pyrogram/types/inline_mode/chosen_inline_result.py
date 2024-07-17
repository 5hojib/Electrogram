from base64 import b64encode
from struct import pack

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from ..update import Update


class ChosenInlineResult(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        result_id: str,
        from_user: "types.User",
        query: str,
        location: "types.Location" = None,
        inline_message_id: str = None,
    ):
        super().__init__(client)

        self.result_id = result_id
        self.from_user = from_user
        self.query = query
        self.location = location
        self.inline_message_id = inline_message_id

    @staticmethod
    def _parse(
        client, chosen_inline_result: raw.types.UpdateBotInlineSend, users
    ) -> "ChosenInlineResult":
        inline_message_id = None

        if isinstance(chosen_inline_result.msg_id, raw.types.InputBotInlineMessageID):
            inline_message_id = (
                b64encode(
                    pack(
                        "<iqq",
                        chosen_inline_result.msg_id.dc_id,
                        chosen_inline_result.msg_id.id,
                        chosen_inline_result.msg_id.access_hash,
                    ),
                    b"-_",
                )
                .decode()
                .rstrip("=")
            )

        return ChosenInlineResult(
            result_id=str(chosen_inline_result.id),
            from_user=types.User._parse(client, users[chosen_inline_result.user_id]),
            query=chosen_inline_result.query,
            location=types.Location(
                longitude=chosen_inline_result.geo.long,
                latitude=chosen_inline_result.geo.lat,
                client=client,
            )
            if chosen_inline_result.geo
            else None,
            inline_message_id=inline_message_id,
        )
