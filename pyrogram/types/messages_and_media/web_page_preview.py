from __future__ import annotations

from pyrogram import raw, types
from pyrogram.types.object import Object


class WebPagePreview(Object):
    """A web page preview.

    Parameters:
        webpage (:obj:`~pyrogram.types.WebPageEmpty` | :obj:`~pyrogram.types.WebPage`):
            Web Page Information.

        force_large_media (``bool``, *optional*):
            True, If the preview media size is forced to large.

        force_small_media  (``bool``, *optional*):
            True, If the preview media size is forced to small.

        is_safe (``bool``, *optional*):
            True, If the webpage is considered safe by telegram.
    """

    def __init__(
        self,
        *,
        webpage: types.WebPage | types.WebPageEmpty,
        force_large_media: bool | None = None,
        force_small_media: bool | None = None,
        invert_media: bool | None = None,
        is_safe: bool | None = None,
    ) -> None:
        super().__init__()

        self.webpage = webpage
        self.force_large_media = force_large_media
        self.force_small_media = force_small_media
        self.invert_media = invert_media
        self.is_safe = is_safe

    @staticmethod
    def _parse(
        client,
        web_page_preview: raw.types.WebPage | raw.types.WebPageEmpty,
        invert_media: bool | None = None,
    ):
        if isinstance(web_page_preview.webpage, raw.types.WebPage):
            webpage = types.WebPage._parse(client, web_page_preview.webpage)
        else:
            webpage = types.WebPageEmpty._parse(web_page_preview.webpage)
        return WebPagePreview(
            webpage=webpage,
            force_large_media=web_page_preview.force_large_media,
            force_small_media=web_page_preview.force_small_media,
            invert_media=invert_media,
            is_safe=web_page_preview.safe,
        )
