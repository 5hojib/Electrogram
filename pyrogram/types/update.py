import pyrogram


class Update:
    @staticmethod
    def stop_propagation():
        raise pyrogram.StopPropagation

    @staticmethod
    def continue_propagation():
        raise pyrogram.ContinuePropagation
