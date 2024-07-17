import asyncio
import logging
import signal
from signal import signal as signal_fn, SIGINT, SIGTERM, SIGABRT

log = logging.getLogger(__name__)

signals = {
    k: v
    for v, k in signal.__dict__.items()
    if v.startswith("SIG") and not v.startswith("SIG_")
}


async def idle():
    task = None

    def signal_handler(signum, __):
        logging.info(f"Stop signal received ({signals[signum]}). Exiting...")
        task.cancel()

    for s in (SIGINT, SIGTERM, SIGABRT):
        signal_fn(s, signal_handler)

    while True:
        task = asyncio.create_task(asyncio.sleep(600))

        try:
            await task
        except asyncio.CancelledError:
            break
