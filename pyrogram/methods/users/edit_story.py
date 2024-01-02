import os
import re
from typing import List

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

class EditStory:
    def _split(self, message, entities, *args, **kwargs):
        return message, entities

    async def edit_story(
        self: "pyrogram.Client",
        story_id: int,
        chat_id: int = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        animation: str = None,
        photo: str = None,
        video: str = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        media_areas: List["types.InputMediaArea"] = None
    ) -> "types.Story":
        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        media = None
        privacy_rules = None

        if privacy:
            privacy_rules = [types.StoriesPrivacyRules(type=privacy)]

        if animation:
            if isinstance(animation, str):
                if os.path.isfile(animation):
                    file = await self.save_file(animation)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(animation) or "video/mp4",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True,
                                duration=0,
                                w=0,
                                h=0
                            ),
                            raw.types.DocumentAttributeAnimated()
                        ]
                    )
                elif re.match("^https?://", animation):
                    media = raw.types.InputMediaDocumentExternal(
                        url=animation
                    )
                else:
                    media = utils.get_input_media_from_file_id(animation, FileType.ANIMATION)
            else:
                file = await self.save_file(animation)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(animation) or "video/mp4",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=True,
                            duration=0,
                            w=0,
                            h=0
                        ),
                        raw.types.DocumentAttributeAnimated()
                    ]
                )
        elif photo:
            if isinstance(photo, str):
                if os.path.isfile(photo):
                    file = await self.save_file(photo)
                    media = raw.types.InputMediaUploadedPhoto(
                        file=file
                    )
                elif re.match("^https?://", photo):
                    media = raw.types.InputMediaPhotoExternal(
                        url=photo
                    )
                else:
                    media = utils.get_input_media_from_file_id(photo, FileType.PHOTO)
            else:
                file = await self.save_file(photo)
                media = raw.types.InputMediaUploadedPhoto(
                    file=file
                )
        elif video:
            if isinstance(video, str):
                if os.path.isfile(video):
                    file = await self.save_file(video)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(video) or "video/mp4",
                        file=file,
                        attributes=[
                            raw.types.DocumentAttributeVideo(
                                supports_streaming=True,
                                duration=0,
                                w=0,
                                h=0
                            )
                        ]
                    )
                elif re.match("^https?://", video):
                    media = raw.types.InputMediaDocumentExternal(
                        url=video
                    )
                else:
                    media = utils.get_input_media_from_file_id(video, FileType.VIDEO)
            else:
                file = await self.save_file(video)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(video) or "video/mp4",
                    file=file,
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=True,
                            duration=0,
                            w=0,
                            h=0
                        )
                    ]
                )
        text = None
        entities = None
        if caption:
            text, entities = self._split(**await utils.parse_text_entities(self, caption, parse_mode, caption_entities))

        if allowed_users and len(allowed_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in allowed_users]
            privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=users))
        if denied_users and len(denied_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in denied_users]
            privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))

        r = await self.invoke(
            raw.functions.stories.EditStory(
                id=story_id,
                peer=peer,
                media=media,
                privacy_rules=privacy_rules,
                caption=text,
                entities=entities,
                media_areas=[
                    await media_area.write(self)
                    for media_area in media_areas
                ]
            )
        )
        return await types.Story._parse(self, r.updates[0].story, r.updates[0].peer)
