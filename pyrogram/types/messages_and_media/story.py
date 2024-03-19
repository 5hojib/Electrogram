import pyrogram

from datetime import datetime
from pyrogram import enums, raw, types, utils
from typing import BinaryIO, Callable, List, Optional, Union
from ..object import Object
from ..update import Update

class Story(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        chat: "types.Chat" = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        date: datetime,
        expire_date: datetime,
        media: "enums.MessageMediaType",
        has_protected_content: bool = None,
        animation: "types.Animation" = None,
        photo: "types.Photo" = None,
        video: "types.Video" = None,
        edited: bool = None,
        pinned: bool = None,
        public: bool = None,
        close_friends: bool = None,
        contacts: bool = None,
        selected_contacts: bool = None,
        caption: str = None,
        caption_entities: List["types.MessageEntity"] = None,
        views: "types.StoryViews" = None,
        privacy: "enums.StoryPrivacy" = None,
        forward_from: "types.StoryForwardHeader" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        media_areas: List["types.MediaArea"] = None,
        raw: "raw.types.StoryItem" = None
    ):
        super().__init__(client)

        self.id = id
        self.chat = chat
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.expire_date = expire_date
        self.media = media
        self.has_protected_content = has_protected_content
        self.animation = animation
        self.photo = photo
        self.video = video
        self.edited = edited
        self.pinned = pinned
        self.public = public
        self.close_friends = close_friends
        self.contacts = contacts
        self.selected_contacts = selected_contacts
        self.caption = caption
        self.caption_entities = caption_entities
        self.views = views
        self.privacy = privacy
        self.forward_from = forward_from
        self.allowed_users = allowed_users
        self.denied_users = denied_users
        self.media_areas = media_areas
        self.raw = raw

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        stories: raw.base.StoryItem,
        peer: Union["raw.types.PeerChannel", "raw.types.PeerUser"]
    ) -> "Story":
        if isinstance(stories, raw.types.StoryItemSkipped):
            return await types.StorySkipped._parse(client, stories, peer)
        if isinstance(stories, raw.types.StoryItemDeleted):
            return await types.StoryDeleted._parse(client, stories, peer)
        entities = [types.MessageEntity._parse(client, entity, {}) for entity in stories.entities]
        entities = types.List(filter(lambda x: x is not None, entities))
        animation = None
        photo = None
        video = None
        chat = None
        from_user = None
        sender_chat = None
        privacy = None
        forward_from = None
        allowed_users = None
        denied_users = None
        if stories.media:
            if isinstance(stories.media, raw.types.MessageMediaPhoto):
                photo = types.Photo._parse(client, stories.media.photo, stories.media.ttl_seconds)
                media_type = enums.MessageMediaType.PHOTO
            elif isinstance(stories.media, raw.types.MessageMediaDocument):
                doc = stories.media.document

                if isinstance(doc, raw.types.Document):
                    attributes = {type(i): i for i in doc.attributes}

                    if raw.types.DocumentAttributeAnimated in attributes:
                        video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                        animation = types.Animation._parse(client, doc, video_attributes, None)
                        media_type = enums.MessageMediaType.ANIMATION
                    elif raw.types.DocumentAttributeVideo in attributes:
                        video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                        video = types.Video._parse(client, doc, video_attributes, None, stories.media.ttl_seconds)
                        media_type = enums.MessageMediaType.VIDEO
                    else:
                        media_type = None
            else:
                media_type = None
        if isinstance(peer, raw.types.PeerChannel) or isinstance(peer, raw.types.InputPeerChannel):
            chat_id = utils.get_channel_id(peer.channel_id)
            chat = await client.invoke(
                raw.functions.channels.GetChannels(
                    id=[await client.resolve_peer(chat_id)]
                )
            )
            if stories.from_id is not None:
                from_user = await client.get_users(stories.from_id.user_id)
                chat = types.Chat._parse_chat(client, chat.chats[0])
            else:
                sender_chat = types.Chat._parse_chat(client, chat.chats[0])
        elif isinstance(peer, raw.types.InputPeerSelf):
            from_user = client.me
        else:
            from_user = await client.get_users(peer.user_id)

        for priv in stories.privacy:
            if isinstance(priv, raw.types.PrivacyValueAllowAll):
                privacy = enums.StoryPrivacy.PUBLIC
            elif isinstance(priv, raw.types.PrivacyValueAllowCloseFriends):
                privacy = enums.StoryPrivacy.CLOSE_FRIENDS
            elif isinstance(priv, raw.types.PrivacyValueAllowContacts):
                privacy = enums.StoryPrivacy.CONTACTS
            elif isinstance(priv, raw.types.PrivacyValueDisallowAll):
                privacy = enums.StoryPrivacy.PRIVATE
            elif isinstance(priv, raw.types.PrivacyValueDisallowContacts):
                privacy = enums.StoryPrivacy.NO_CONTACTS

            if isinstance(priv, raw.types.PrivacyValueAllowUsers):
                allowed_users = priv.users
            if isinstance(priv, raw.types.PrivacyValueDisallowUsers):
                denied_users = priv.users

        if stories.fwd_from is not None:
            forward_from = await types.StoryForwardHeader._parse(client, stories.fwd_from)

        media_areas = None
        if stories.media_areas is not None and len(stories.media_areas) > 0:
            media_areas = [
                await types.MediaArea._parse(client, media_area)
                for media_area in stories.media_areas
            ]

        return Story(
            id=stories.id,
            chat=chat,
            from_user=from_user,
            sender_chat=sender_chat,
            date=utils.timestamp_to_datetime(stories.date),
            expire_date=utils.timestamp_to_datetime(stories.expire_date),
            media=media_type,
            has_protected_content=stories.noforwards,
            animation=animation,
            photo=photo,
            video=video,
            edited=stories.edited,
            pinned=stories.pinned,
            public=stories.public,
            close_friends=stories.close_friends,
            contacts=stories.contacts,
            selected_contacts=stories.selected_contacts,
            caption=stories.caption,
            caption_entities=entities or None,
            views=types.StoryViews._parse(stories.views),
            privacy=privacy,
            forward_from=forward_from,
            allowed_users=allowed_users,
            denied_users=denied_users,
            media_areas=media_areas,
            raw=stories,
            client=client
        )

    async def reply_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup=None
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_message(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_story_id: int = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_animation(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            animation=animation,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_audio(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            audio=audio,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            performer=performer,
            title=title,
            thumb=thumb,
            file_name=file_name,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_cached_media(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup
        )

    async def reply_media_group(
        self,
        media: List[Union[
            "types.InputMediaPhoto",
            "types.InputMediaVideo",
            "types.InputMediaAudio",
            "types.InputMediaDocument"
        ]],
        disable_notification: bool = None,
        reply_to_story_id: int = None
    ) -> List["types.Message"]:
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_media_group(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            media=media,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id
        )

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_photo(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_sticker(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            sticker=sticker,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        duration: int = 0,
        width: int = 0,
        height: int = 0,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        supports_streaming: bool = True,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_video(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            duration=duration,
            width=width,
            height=height,
            thumb=thumb,
            file_name=file_name,
            supports_streaming=supports_streaming,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_video_note(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_story_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "types.Message":
        if reply_to_story_id is None:
            reply_to_story_id = self.id

        return await self._client.send_voice(
            chat_id=self.from_user.id if self.from_user else self.sender_chat.id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            reply_to_story_id=reply_to_story_id,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def delete(self):
        return await self._client.delete_stories(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_ids=self.id
        )

    async def edit_animation(
        self,
        animation: Union[str, BinaryIO]
    ) -> "types.Story":
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            animation=animation
        )

    async def edit(
        self,
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
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users,
            animation=animation,
            photo=photo,
            video=video,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            media_areas=media_areas
        )

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None
    ) -> "types.Story":
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities
        )

    async def edit_photo(
        self,
        photo: Union[str, BinaryIO]
    ) -> "types.Story":
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            photo=photo
        )

    async def edit_privacy(
        self,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
    ) -> "types.Story":
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users
        )

    async def edit_video(
        self,
        video: Union[str, BinaryIO]
    ) -> "types.Story":
        return await self._client.edit_story(
            chat_id=self.sender_chat.id if self.sender_chat else None,
            story_id=self.id,
            video=video
        )

    async def export_link(self) -> "types.ExportedStoryLink":
        return await self._client.export_story_link(chat_id=self.from_user.id if self.from_user else self.sender_chat.id, story_id=self.id)

    async def forward(
        self,
        chat_id: int = None,
        privacy: "enums.StoriesPrivacyRules" = None,
        allowed_users: List[int] = None,
        denied_users: List[int] = None,
        pinned: bool = None,
        protect_content: bool = None,
        caption: str = None,
        parse_mode: "enums.ParseMode" = None,
        caption_entities: List["types.MessageEntity"] = None,
        period: int = None
    ):
        return await self._client.send_story(
            chat_id=chat_id,
            privacy=privacy,
            allowed_users=allowed_users,
            denied_users=denied_users,
            pinned=pinned,
            protect_content=protect_content,
            caption=caption,
            caption_entities=caption_entities,
            parse_mode=parse_mode,
            period=period,
            forward_from_chat_id=self.from_user.id if self.from_user is not None else self.sender_chat.id,
            forward_from_story_id=self.id
        )

    async def download(
        self,
        file_name: str = "",
        in_memory: bool = False,
        block: bool = True,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> str:
        return await self._client.download_media(
            message=self,
            file_name=file_name,
            in_memory=in_memory,
            block=block,
            progress=progress,
            progress_args=progress_args,
        )
