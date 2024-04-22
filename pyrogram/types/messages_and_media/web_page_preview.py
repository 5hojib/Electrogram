import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from typing import Union


class WebPagePreview(Object):
    def __init__(
        self,
        *,
        webpage: Union["types.WebPage", "types.WebPageEmpty"],
        force_large_media: bool = None,
        force_small_media: bool = None,
        invert_media: bool = None,
        is_safe: bool = None
    ):
        super().__init__()

        self.webpage = webpage
        self.force_large_media = force_large_media
        self.force_small_media = force_small_media
        self.invert_media = invert_media
        self.is_safe = is_safe

    @staticmethod
    def _parse(
        client,
        web_page_preview: Union["raw.types.WebPage", "raw.types.WebPageEmpty"],
        invert_media: bool = None
    ):
        if isinstance(web_page_preview.webpage, raw.types.WebPage):
            webpage=types.WebPage._parse(client, web_page_preview.webpage)
        else:
            webpage=types.WebPageEmpty._parse(web_page_preview.webpage)
        return WebPagePreview(
            webpage=webpage,
            force_large_media=web_page_preview.force_large_media,
            force_small_media=web_page_preview.force_small_media,
            invert_media=invert_media,
            is_safe=web_page_preview.safe
        )