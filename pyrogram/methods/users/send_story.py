import os
import re
from typing import BinaryIO, List, Union

import pyrogram
from pyrogram import enums, raw, types, utils
from pyrogram.file_id import FileType

class SendStory:
    def _split(self, message, entities, *args, **kwargs):
        return message, entities

    async def send_story(
        self: "pyrogram.Client",
        chat_id: Union[int,str] = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        #allowed_chats: List[int] = None,
        #denied_chats: List[int] = None,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        file_name: str = None,
        pinned: bool = None,
        protect_content: bool = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        period: int = None,
        forward_from_chat_id: Union[int, str] = None,
        forward_from_story_id: int = None,
        media_areas: List["types.InputMediaArea"] = None
    ) -> "types.Story":
        if chat_id:
            peer = await self.resolve_peer(chat_id)
        else:
            peer = await self.resolve_peer("me")

        if privacy:
            privacy_rules = [types.StoriesPrivacyRules(type=privacy)]
        else:
            privacy_rules = [types.StoriesPrivacyRules(type=enums.StoriesPrivacyRules.PUBLIC)]

        if photo:
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
                    video = await self.download_media(video, in_memory=True)
                    file = await self.save_file(video)
                    media = raw.types.InputMediaUploadedDocument(
                        mime_type=self.guess_mime_type(file_name or video.name) or "video/mp4",
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
            else:
                file = await self.save_file(video)
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(file_name or video.name) or "video/mp4",
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
        else:
            if forward_from_chat_id is None:
                raise ValueError("You need to pass one of the following parameter animation/photo/video/forward_from_chat_id!")
        
        text, entities = self._split(**await utils.parse_text_entities(self, caption, parse_mode, caption_entities))

        if allowed_users and len(allowed_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in allowed_users]
            privacy_rules.append(raw.types.InputPrivacyValueAllowUsers(users=users))
        if denied_users and len(denied_users) > 0:
            users = [await self.resolve_peer(user_id) for user_id in denied_users]
            privacy_rules.append(raw.types.InputPrivacyValueDisallowUsers(users=users))

        forward_from_chat = None
        if forward_from_chat_id is not None:
            forward_from_chat = await self.resolve_peer(forward_from_chat_id)
            media = raw.types.InputMediaEmpty()
            if forward_from_story_id is None:
                raise ValueError("You need to pass forward_from_story_id to forward story!")

        r = await self.invoke(
            raw.functions.stories.SendStory(
                peer=peer,
                media=media,
                privacy_rules=privacy_rules,
                random_id=self.rnd_id(),
                pinned=pinned,
                noforwards=protect_content,
                caption=text,
                entities=entities,
                period=period,
                fwd_from_id=forward_from_chat,
                fwd_from_story=forward_from_story_id if forward_from_chat_id is not None else None,
                fwd_modified=True if forward_from_chat_id is not None and caption is not None else False,
                media_areas=[
                    await media_area.write(self)
                    for media_area in media_areas
                ] if media_areas is not None else None
            )
        )
        return await types.Story._parse(self, r.updates[0].story, r.updates[0].peer)
