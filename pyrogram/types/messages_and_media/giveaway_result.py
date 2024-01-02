import pyrogram

from datetime import datetime
from pyrogram import raw, types, utils
from ..object import Object
from typing import List, Union


class GiveawayResult(Object):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat" = None,
        giveaway_message: "types.Message" = None,
        quantity: int,
        unclaimed_quantity: int,
        winners: List["types.User"] = None,
        months: int = None,
        expire_date: datetime = None,
        new_subscribers : bool = None,
        is_refunded: bool = None,
        is_winners_hidden: bool
    ):
        super().__init__(client)

        self.chat = chat
        self.giveaway_message = giveaway_message
        self.quantity = quantity
        self.unclaimed_quantity = unclaimed_quantity
        self.winners = winners
        self.months = months
        self.expire_date = expire_date
        self.new_subscribers = new_subscribers
        self.is_refunded = is_refunded
        self.is_winners_hidden = is_winners_hidden

    @staticmethod
    async def _parse(
        client,
        giveaway_result: Union[
            "raw.types.MessageActionGiveawayResults",
            "raw.types.MessageMediaGiveawayResults"
        ],
        hide_winners: bool = False
    ) -> "GiveawayResult":
        chat = None
        giveaway_message = None
        expired_date = None
        winners = None
        if not hide_winners:
            chat_id = utils.get_channel_id(giveaway_result.channel_id)
            chat = await client.invoke(
                raw.functions.channels.GetChannels(
                    id=[await client.resolve_peer(chat_id)]
                )
            )
            chat = types.Chat._parse_chat(client, chat.chats[0])
            giveaway_message = await client.get_messages(chat_id, giveaway_result.launch_msg_id)
            expired_date = utils.timestamp_to_datetime(giveaway_result.until_date)
            winners = []
            for winner in giveaway_result.winners:
                winners.append(await client.get_users(winner))

        return GiveawayResult(
            chat=chat,
            giveaway_message=giveaway_message,
            quantity=getattr(giveaway_result, "winners_count", None),
            unclaimed_quantity=getattr(giveaway_result, "unclaimed_count", None),
            winners=winners,
            months=getattr(giveaway_result, "months", None),
            expire_date=expired_date,
            new_subscribers=getattr(giveaway_result, "only_new_subscribers", None),
            is_refunded=getattr(giveaway_result, "refunded", None),
            is_winners_hidden=hide_winners,
            client=client
        )