from __future__ import annotations

from typing import NoReturn

import pyrogram


class StopTransmissionError:
    @staticmethod
    def stop_transmission() -> NoReturn:
        """Stop downloading or uploading a file.

        This method must be called inside a progress callback function in order to stop the transmission at the
        desired time. The progress callback is called every time a file chunk is uploaded/downloaded.

        Example:
            .. code-block:: python

                # Stop transmission once the upload progress reaches 50%
                async def progress(current, total, client):
                    if (current * 100 / total) > 50:
                        client.stop_transmission()

                async with app:
                    await app.send_document(
                        "me", "file.zip",
                        progress=progress,
                        progress_args=(app,))
        """
        raise pyrogram.StopTransmissionError
