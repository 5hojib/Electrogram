from __future__ import annotations

from typing import NoReturn

import pyrogram


class Update:
    @staticmethod
    def stop_propagation() -> NoReturn:
        raise pyrogram.StopPropagationError

    @staticmethod
    def continue_propagation() -> NoReturn:
        raise pyrogram.ContinuePropagationError
