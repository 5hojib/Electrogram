import pyrogram


class StopTransmission:
    @staticmethod
    def stop_transmission():
        raise pyrogram.StopTransmission
