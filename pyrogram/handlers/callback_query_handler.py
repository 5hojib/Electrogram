import pyrogram
from asyncio import iscoroutinefunction
from typing import Callable, Tuple
from pyrogram.utils import PyromodConfig
from pyrogram.types import CallbackQuery, Identifier, Listener
from .handler import Handler

class CallbackQueryHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future_or_callback, filters)

    def compose_data_identifier(self, query: CallbackQuery):
        from_user = query.from_user
        from_user_id = from_user.id if from_user else None
        from_user_username = from_user.username if from_user else None
        chat_id = None
        message_id = None

        if query.message:
            message_id = getattr(query.message, "id", getattr(query.message, "message_id", None))

            if query.message.chat:
                chat_id = [query.message.chat.id, query.message.chat.username]

        return Identifier(
            message_id=message_id,
            chat_id=chat_id,
            from_user_id=[from_user_id, from_user_username],
            inline_message_id=query.inline_message_id,
        )

    async def check_if_has_matching_listener(self, client: "pyrogram.Client", query: CallbackQuery) -> Tuple[bool, Listener]:
        data = self.compose_data_identifier(query)
        listener = client.get_listener_matching_with_data(data, pyrogram.enums.ListenerTypes.CALLBACK_QUERY)
        listener_does_match = False

        if listener:
            filters = listener.filters
            if callable(filters):
                if iscoroutinefunction(filters.__call__):
                    listener_does_match = await filters(client, query)
                else:
                    listener_does_match = await client.loop.run_in_executor(None, filters, client, query)
            else:
                listener_does_match = True

        return listener_does_match, listener

    async def check(self, client: "pyrogram.Client", query: CallbackQuery):
        listener_does_match, listener = await self.check_if_has_matching_listener(client, query)

        if callable(self.filters):
            if iscoroutinefunction(self.filters.__call__):
                handler_does_match = await self.filters(client, query)
            else:
                handler_does_match = await client.loop.run_in_executor(None, self.filters, client, query)
        else:
            handler_does_match = True

        data = self.compose_data_identifier(query)

        if PyromodConfig.unallowed_click_alert:
            permissive_identifier = Identifier(
                chat_id=data.chat_id,
                message_id=data.message_id,
                inline_message_id=data.inline_message_id,
                from_user_id=None,
            )
            matches = permissive_identifier.matches(data)

            if listener and (matches and not listener_does_match) and listener.unallowed_click_alert:
                alert = listener.unallowed_click_alert if isinstance(listener.unallowed_click_alert, str) else PyromodConfig.unallowed_click_alert_text
                await query.answer(alert)
                return False

        return listener_does_match or handler_does_match

    async def resolve_future_or_callback(self, client: "pyrogram.Client", query: CallbackQuery, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(client, query)

        if listener and listener_does_match:
            client.remove_listener(listener)

            if listener.future and not listener.future.done():
                listener.future.set_result(query)
                raise pyrogram.StopPropagation
            elif listener.callback:
                if iscoroutinefunction(listener.callback):
                    await listener.callback(client, query, *args)
                else:
                    listener.callback(client, query, *args)

                raise pyrogram.StopPropagation
            else:
                raise ValueError("Listener must have either a future or a callback")
        else:
            await self.original_callback(client, query, *args)
