from typing import NoReturn

import pyrogram


class Update:
    @staticmethod
    def stop_propagation() -> NoReturn:
        raise pyrogram.StopPropagation

    @staticmethod
    def continue_propagation() -> NoReturn:
        raise pyrogram.ContinuePropagation
