from inspect import iscoroutinefunction
from typing import Callable
import pyrogram
from pyrogram.types import Message, Identifier
from .handler import Handler

class MessageHandler(Handler):
    def __init__(self, callback: Callable, filters=None):
        self.original_callback = callback
        super().__init__(self.resolve_future_or_callback, filters)

    async def check_if_has_matching_listener(self, client: "pyrogram.Client", message: Message):
        from_user = message.from_user
        from_user_id = from_user.id if from_user else None
        from_user_username = from_user.username if from_user else None

        message_id = getattr(message, "id", getattr(message, "message_id", None))

        data = Identifier(
            message_id=message_id,
            chat_id=[message.chat.id, message.chat.username],
            from_user_id=[from_user_id, from_user_username],
        )

        listener = client.get_listener_matching_with_data(data, pyrogram.enums.ListenerTypes.MESSAGE)

        listener_does_match = False

        if listener:
            filters = listener.filters
            if callable(filters):
                if iscoroutinefunction(filters.__call__):
                    listener_does_match = await filters(client, message)
                else:
                    listener_does_match = await client.loop.run_in_executor(
                        None, filters, client, message
                    )
            else:
                listener_does_match = True

        return listener_does_match, listener

    async def check(self, client: "pyrogram.Client", message: Message):
        listener_does_match = (
            await self.check_if_has_matching_listener(client, message)
        )[0]

        if callable(self.filters):
            if iscoroutinefunction(self.filters.__call__):
                handler_does_match = await self.filters(client, message)
            else:
                handler_does_match = await client.loop.run_in_executor(
                    None, self.filters, client, message
                )
        else:
            handler_does_match = True

        return listener_does_match or handler_does_match

    async def resolve_future_or_callback(self, client: "pyrogram.Client", message: Message, *args):
        listener_does_match, listener = await self.check_if_has_matching_listener(
            client, message
        )

        if listener and listener_does_match:
            client.remove_listener(listener)

            if listener.future and not listener.future.done():
                listener.future.set_result(message)

                raise pyrogram.StopPropagation
            elif listener.callback:
                if iscoroutinefunction(listener.callback):
                    await listener.callback(client, message, *args)
                else:
                    listener.callback(client, message, *args)

                raise pyrogram.StopPropagation
            else:
                raise ValueError("Listener must have either a future or a callback")
        else:
            await self.original_callback(client, message, *args)
