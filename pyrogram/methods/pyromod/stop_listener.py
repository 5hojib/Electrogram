import inspect
import pyrogram

from pyrogram.errors import ListenerStopped
from pyrogram.types import Listener
from pyrogram.utils import PyromodConfig

class StopListener:
    async def stop_listener(
        self: "pyrogram.Client",
        listener: Listener
    ):
        self.remove_listener(listener)

        if listener.future.done():
            return

        if callable(PyromodConfig.stopped_handler):
            if inspect.iscoroutinefunction(PyromodConfig.stopped_handler.__call__):
                await PyromodConfig.stopped_handler(None, listener)
            else:
                await self.loop.run_in_executor(
                    None, PyromodConfig.stopped_handler, None, listener
                )
        elif PyromodConfig.throw_exceptions:
            listener.future.set_exception(ListenerStopped())
