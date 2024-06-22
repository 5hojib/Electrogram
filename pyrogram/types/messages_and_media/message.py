import logging
from datetime import datetime
from functools import partial
from typing import List, Match, Union, BinaryIO, Optional, Callable

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import ChannelPrivate, MessageIdsEmpty, PeerIdInvalid
from pyrogram.parser import utils as parser_utils, Parser
from ..object import Object
from ..update import Update

log = logging.getLogger(__name__)


class Str(str):
    def __init__(self, *args):
        super().__init__()

        self.entities = None

    def init(self, entities):
        self.entities = entities

        return self

    @property
    def markdown(self):
        return Parser.unparse(self, self.entities, False)

    @property
    def html(self):
        return Parser.unparse(self, self.entities, True)

    def __getitem__(self, item):
        return parser_utils.remove_surrogates(parser_utils.add_surrogates(self)[item])


class Message(Object, Update):
    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: int,
        message_thread_id: int = None,
        from_user: "types.User" = None,
        sender_chat: "types.Chat" = None,
        date: datetime = None,
        chat: "types.Chat" = None,
        topics: "types.ForumTopic" = None,
        forward_from: "types.User" = None,
        forward_sender_name: str = None,
        forward_from_chat: "types.Chat" = None,
        forward_from_message_id: int = None,
        forward_signature: str = None,
        forward_date: datetime = None,
        is_topic_message: bool = None,
        reply_to_message_id: int = None,
        reply_to_story_id: int = None,
        reply_to_story_user_id: int = None,
        reply_to_story_chat_id: int = None,
        reply_to_top_message_id: int = None,
        reply_to_message: "Message" = None,
        reply_to_story: "types.Story" = None,
        mentioned: bool = None,
        empty: bool = None,
        service: "enums.MessageServiceType" = None,
        scheduled: bool = None,
        from_scheduled: bool = None,
        edit_hide: bool = None,
        media: "enums.MessageMediaType" = None,
        edit_date: datetime = None,
        media_group_id: str = None,
        author_signature: str = None,
        has_protected_content: bool = None,
        has_media_spoiler: bool = None,
        text: Str = None,
        entities: List["types.MessageEntity"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        effect_id: str = None,
        invert_media: bool = None,
        audio: "types.Audio" = None,
        document: "types.Document" = None,
        photo: "types.Photo" = None,
        sticker: "types.Sticker" = None,
        animation: "types.Animation" = None,
        game: "types.Game" = None,
        giveaway: "types.Giveaway" = None,
        giveaway_result: "types.GiveawayResult" = None,
        boosts_applied: int = None,
        story: Union["types.MessageStory", "types.Story"] = None,
        video: "types.Video" = None,
        voice: "types.Voice" = None,
        video_note: "types.VideoNote" = None,
        web_page_preview: "types.WebPagePreview" = None,
        caption: Str = None,
        contact: "types.Contact" = None,
        location: "types.Location" = None,
        venue: "types.Venue" = None,
        poll: "types.Poll" = None,
        dice: "types.Dice" = None,
        new_chat_members: List["types.User"] = None,
        chat_joined_by_request: "types.ChatJoinedByRequest" = None,
        left_chat_member: "types.User" = None,
        new_chat_title: str = None,
        new_chat_photo: "types.Photo" = None,
        delete_chat_photo: bool = None,
        group_chat_created: bool = None,
        supergroup_chat_created: bool = None,
        channel_chat_created: bool = None,
        migrate_to_chat_id: int = None,
        migrate_from_chat_id: int = None,
        pinned_message: "Message" = None,
        game_high_score: int = None,
        views: int = None,
        forwards: int = None,
        via_bot: "types.User" = None,
        outgoing: bool = None,
        matches: List[Match] = None,
        command: List[str] = None,
        chat_shared: List[int] = None,
        user_shared: List[int] = None,
        forum_topic_created: "types.ForumTopicCreated" = None,
        forum_topic_closed: "types.ForumTopicClosed" = None,
        forum_topic_reopened: "types.ForumTopicReopened" = None,
        forum_topic_edited: "types.ForumTopicEdited" = None,
        general_topic_hidden: "types.GeneralTopicHidden" = None,
        general_topic_unhidden: "types.GeneralTopicUnhidden" = None,
        giveaway_launched: "types.GiveawayLaunched" = None,
        video_chat_scheduled: "types.VideoChatScheduled" = None,
        video_chat_started: "types.VideoChatStarted" = None,
        video_chat_ended: "types.VideoChatEnded" = None,
        video_chat_members_invited: "types.VideoChatMembersInvited" = None,
        web_app_data: "types.WebAppData" = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reactions: List["types.Reaction"] = None,
        raw: "raw.types.Message" = None
    ):
        super().__init__(client)

        self.id = id
        self.message_thread_id = message_thread_id
        self.from_user = from_user
        self.sender_chat = sender_chat
        self.date = date
        self.chat = chat
        self.topics = topics
        self.forward_from = forward_from
        self.forward_sender_name = forward_sender_name
        self.forward_from_chat = forward_from_chat
        self.forward_from_message_id = forward_from_message_id
        self.forward_signature = forward_signature
        self.forward_date = forward_date
        self.is_topic_message = is_topic_message
        self.reply_to_message_id = reply_to_message_id
        self.reply_to_story_id = reply_to_story_id
        self.reply_to_story_user_id = reply_to_story_user_id
        self.reply_to_story_chat_id = reply_to_story_chat_id
        self.reply_to_top_message_id = reply_to_top_message_id
        self.reply_to_message = reply_to_message
        self.reply_to_story = reply_to_story
        self.mentioned = mentioned
        self.empty = empty
        self.service = service
        self.scheduled = scheduled
        self.from_scheduled = from_scheduled
        self.media = media
        self.edit_date = edit_date
        self.edit_hide = edit_hide
        self.media_group_id = media_group_id
        self.author_signature = author_signature
        self.has_protected_content = has_protected_content
        self.has_media_spoiler = has_media_spoiler
        self.text = text
        self.entities = entities
        self.caption_entities = caption_entities
        self.quote_text = quote_text
        self.quote_entities = quote_entities
        self.effect_id = effect_id
        self.invert_media = invert_media
        self.audio = audio
        self.document = document
        self.photo = photo
        self.sticker = sticker
        self.animation = animation
        self.game = game
        self.giveaway = giveaway
        self.giveaway_result = giveaway_result
        self.boosts_applied = boosts_applied
        self.story = story
        self.video = video
        self.voice = voice
        self.video_note = video_note
        self.web_page_preview = web_page_preview
        self.caption = caption
        self.contact = contact
        self.location = location
        self.venue = venue
        self.poll = poll
        self.dice = dice
        self.new_chat_members = new_chat_members
        self.chat_joined_by_request = chat_joined_by_request
        self.left_chat_member = left_chat_member
        self.new_chat_title = new_chat_title
        self.new_chat_photo = new_chat_photo
        self.delete_chat_photo = delete_chat_photo
        self.group_chat_created = group_chat_created
        self.supergroup_chat_created = supergroup_chat_created
        self.channel_chat_created = channel_chat_created
        self.migrate_to_chat_id = migrate_to_chat_id
        self.migrate_from_chat_id = migrate_from_chat_id
        self.pinned_message = pinned_message
        self.game_high_score = game_high_score
        self.views = views
        self.forwards = forwards
        self.via_bot = via_bot
        self.outgoing = outgoing
        self.matches = matches
        self.command = command
        self.reply_markup = reply_markup
        self.chat_shared = chat_shared
        self.user_shared = user_shared
        self.forum_topic_created = forum_topic_created
        self.forum_topic_closed = forum_topic_closed
        self.forum_topic_reopened = forum_topic_reopened
        self.forum_topic_edited = forum_topic_edited
        self.general_topic_hidden = general_topic_hidden
        self.general_topic_unhidden = general_topic_unhidden
        self.giveaway_launched = giveaway_launched
        self.video_chat_scheduled = video_chat_scheduled
        self.video_chat_started = video_chat_started
        self.video_chat_ended = video_chat_ended
        self.video_chat_members_invited = video_chat_members_invited
        self.web_app_data = web_app_data
        self.reactions = reactions
        self.raw = raw

    async def wait_for_click(
            self,
            from_user_id: Optional[Union[Union[int, str], List[Union[int, str]]]] = None,
            timeout: Optional[int] = None,
            filters=None,
            alert: Union[str, bool] = True,
    ):
        message_id = getattr(self, "id", getattr(self, "message_id", None))

        return await self._client.listen(
            filters=filters,
            timeout=timeout,
            listener_type=pyrogram.enums.ListenerTypes.CALLBACK_QUERY,
            unallowed_click_alert=alert,
            chat_id=self.chat.id,
            user_id=from_user_id,
            message_id=message_id,
        )

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        message: raw.base.Message,
        users: dict,
        chats: dict,
        topics: dict = None,
        is_scheduled: bool = False,
        replies: int = 1
    ):
        if isinstance(message, raw.types.MessageEmpty):
            return Message(id=message.id, empty=True, client=client, raw=message)

        from_id = utils.get_raw_peer_id(message.from_id)
        peer_id = utils.get_raw_peer_id(message.peer_id)
        user_id = from_id or peer_id

        if isinstance(message.from_id, raw.types.PeerUser) and isinstance(message.peer_id, raw.types.PeerUser):
            if from_id not in users or peer_id not in users:
                try:
                    r = await client.invoke(
                        raw.functions.users.GetUsers(
                            id=[
                                await client.resolve_peer(from_id),
                                await client.resolve_peer(peer_id)
                            ]
                        )
                    )
                except PeerIdInvalid:
                    pass
                else:
                    users.update({i.id: i for i in r})

        if isinstance(message, raw.types.MessageService):
            message_thread_id = None
            action = message.action

            new_chat_members = None
            chat_joined_by_request = None
            left_chat_member = None
            new_chat_title = None
            delete_chat_photo = None
            migrate_to_chat_id = None
            migrate_from_chat_id = None
            group_chat_created = None
            channel_chat_created = None
            new_chat_photo = None
            chat_shared = None
            user_shared = None
            is_topic_message = None
            forum_topic_created = None
            forum_topic_closed = None
            forum_topic_reopened = None
            forum_topic_edited = None
            general_topic_hidden = None
            general_topic_unhidden = None
            video_chat_scheduled = None
            video_chat_started = None
            video_chat_ended = None
            video_chat_members_invited = None
            web_app_data = None
            giveaway_launched = None
            giveaway_result = None
            boosts_applied = None

            service_type = None

            if isinstance(action, raw.types.MessageActionChatAddUser):
                new_chat_members = [types.User._parse(client, users[i]) for i in action.users]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatJoinedByLink):
                new_chat_members = [types.User._parse(client, users[utils.get_raw_peer_id(message.from_id)])]
                service_type = enums.MessageServiceType.NEW_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatJoinedByRequest):
                chat_joined_by_request = types.ChatJoinedByRequest()
                service_type = enums.MessageServiceType.CHAT_JOINED_BY_REQUEST
            elif isinstance(action, raw.types.MessageActionChatDeleteUser):
                left_chat_member = types.User._parse(client, users[action.user_id])
                service_type = enums.MessageServiceType.LEFT_CHAT_MEMBERS
            elif isinstance(action, raw.types.MessageActionChatEditTitle):
                new_chat_title = action.title
                service_type = enums.MessageServiceType.NEW_CHAT_TITLE
            elif isinstance(action, raw.types.MessageActionChatDeletePhoto):
                delete_chat_photo = True
                service_type = enums.MessageServiceType.DELETE_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionChatMigrateTo):
                migrate_to_chat_id = action.channel_id
                service_type = enums.MessageServiceType.MIGRATE_TO_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChannelMigrateFrom):
                migrate_from_chat_id = action.chat_id
                service_type = enums.MessageServiceType.MIGRATE_FROM_CHAT_ID
            elif isinstance(action, raw.types.MessageActionChatCreate):
                group_chat_created = True
                service_type = enums.MessageServiceType.GROUP_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChannelCreate):
                channel_chat_created = True
                service_type = enums.MessageServiceType.CHANNEL_CHAT_CREATED
            elif isinstance(action, raw.types.MessageActionChatEditPhoto):
                new_chat_photo = types.Photo._parse(client, action.photo)
                service_type = enums.MessageServiceType.NEW_CHAT_PHOTO
            elif isinstance(action, raw.types.MessageActionRequestedPeer):
                chat_shared = []
                user_shared = []
                for peer in action.peers:
                    if isinstance(peer, raw.types.PeerChannel):
                        chat_shared.append(utils.get_channel_id(utils.get_raw_peer_id(peer)))
                        service_type = enums.MessageServiceType.ChannelShared
                    elif isinstance(peer, raw.types.PeerChat):
                        chat_shared.append(utils.get_channel_id(utils.get_raw_peer_id(peer)))
                        service_type = enums.MessageServiceType.ChannelShared
                    elif isinstance(peer, raw.types.PeerUser):
                        user_shared.append(peer.user_id)
                        service_type = enums.MessageServiceType.UserShared
            elif isinstance(action, raw.types.MessageActionTopicCreate):
                forum_topic_created = types.ForumTopicCreated._parse(message)
                service_type = enums.MessageServiceType.FORUM_TOPIC_CREATED
            elif isinstance(action, raw.types.MessageActionTopicEdit):
                if action.title:
                    forum_topic_edited = types.ForumTopicEdited._parse(action)
                    service_type = enums.MessageServiceType.FORUM_TOPIC_EDITED
                elif action.hidden:
                    general_topic_hidden = types.GeneralTopicHidden()
                    service_type = enums.MessageServiceType.GENERAL_TOPIC_HIDDEN
                elif action.closed:
                    forum_topic_closed = types.ForumTopicClosed()
                    service_type = enums.MessageServiceType.FORUM_TOPIC_CLOSED
                else:
                    if hasattr(action, "hidden") and action.hidden is not None:
                        general_topic_unhidden = types.GeneralTopicUnhidden()
                        service_type = enums.MessageServiceType.GENERAL_TOPIC_UNHIDDEN
                    else:
                        forum_topic_reopened = types.ForumTopicReopened()
                        service_type = enums.MessageServiceType.FORUM_TOPIC_REOPENED
            elif isinstance(action, raw.types.MessageActionGroupCallScheduled):
                video_chat_scheduled = types.VideoChatScheduled._parse(action)
                service_type = enums.MessageServiceType.VIDEO_CHAT_SCHEDULED
            elif isinstance(action, raw.types.MessageActionGroupCall):
                if action.duration:
                    video_chat_ended = types.VideoChatEnded._parse(action)
                    service_type = enums.MessageServiceType.VIDEO_CHAT_ENDED
                else:
                    video_chat_started = types.VideoChatStarted()
                    service_type = enums.MessageServiceType.VIDEO_CHAT_STARTED
            elif isinstance(action, raw.types.MessageActionInviteToGroupCall):
                video_chat_members_invited = types.VideoChatMembersInvited._parse(client, action, users)
                service_type = enums.MessageServiceType.VIDEO_CHAT_MEMBERS_INVITED
            elif isinstance(action, raw.types.MessageActionWebViewDataSentMe):
                web_app_data = types.WebAppData._parse(action)
                service_type = enums.MessageServiceType.WEB_APP_DATA
            elif isinstance(action, raw.types.MessageActionGiveawayLaunch):
                giveaway_launched = types.GiveawayLaunched()
                service_type = enums.MessageServiceType.GIVEAWAY_LAUNCHED
            elif isinstance(action, raw.types.MessageActionGiveawayResults):
                giveaway_result = await types.GiveawayResult._parse(client, action, True)
                service_type = enums.MessageServiceType.GIVEAWAY_RESULT
            elif isinstance(action, raw.types.MessageActionBoostApply):
                boosts_applied = action.boosts
                service_type = enums.MessageServiceType.BOOST_APPLY
            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                topics=None,
                from_user=from_user,
                sender_chat=sender_chat,
                service=service_type,
                new_chat_members=new_chat_members,
                chat_joined_by_request=chat_joined_by_request,
                left_chat_member=left_chat_member,
                new_chat_title=new_chat_title,
                new_chat_photo=new_chat_photo,
                delete_chat_photo=delete_chat_photo,
                migrate_to_chat_id=utils.get_channel_id(migrate_to_chat_id) if migrate_to_chat_id else None,
                migrate_from_chat_id=-migrate_from_chat_id if migrate_from_chat_id else None,
                group_chat_created=group_chat_created,
                channel_chat_created=channel_chat_created,
                chat_shared=chat_shared if chat_shared is not None and len(chat_shared) > 0 else None,
                user_shared=user_shared if user_shared is not None and len(user_shared) > 0 else None,
                is_topic_message=is_topic_message,
                forum_topic_created=forum_topic_created,
                forum_topic_closed=forum_topic_closed,
                forum_topic_reopened=forum_topic_reopened,
                forum_topic_edited=forum_topic_edited,
                general_topic_hidden=general_topic_hidden,
                general_topic_unhidden=general_topic_unhidden,
                video_chat_scheduled=video_chat_scheduled,
                video_chat_started=video_chat_started,
                video_chat_ended=video_chat_ended,
                video_chat_members_invited=video_chat_members_invited,
                web_app_data=web_app_data,
                giveaway_launched=giveaway_launched,
                giveaway_result=giveaway_result,
                boosts_applied=boosts_applied,
                raw=message,
                client=client
            )

            if isinstance(action, raw.types.MessageActionPinMessage):
                try:
                    parsed_message.pinned_message = await client.get_messages(
                        parsed_message.chat.id,
                        reply_to_message_ids=message.id,
                        replies=0
                    )

                    parsed_message.service = enums.MessageServiceType.PINNED_MESSAGE
                except MessageIdsEmpty:
                    pass

            if isinstance(action, raw.types.MessageActionGameScore):
                parsed_message.game_high_score = types.GameHighScore._parse_action(client, message, users)

                if message.reply_to and replies:
                    try:
                        parsed_message.reply_to_message = await client.get_messages(
                            parsed_message.chat.id,
                            reply_to_message_ids=message.id,
                            replies=0
                        )

                        parsed_message.service = enums.MessageServiceType.GAME_HIGH_SCORE
                    except MessageIdsEmpty:
                        pass

            client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            if message.reply_to:
                if message.reply_to.forum_topic:
                    if message.reply_to.reply_to_top_id:
                        parsed_message.message_thread_id = message.reply_to.reply_to_top_id
                    else:
                        parsed_message.message_thread_id = message.reply_to.reply_to_msg_id
                    parsed_message.is_topic_message = True

            return parsed_message

        if isinstance(message, raw.types.Message):
            message_thread_id = None
            entities = [types.MessageEntity._parse(client, entity, users) for entity in message.entities]
            entities = types.List(filter(lambda x: x is not None, entities))

            forward_from = None
            forward_sender_name = None
            forward_from_chat = None
            forward_from_message_id = None
            forward_signature = None
            forward_date = None
            is_topic_message = None

            forward_header = message.fwd_from

            if forward_header:
                forward_date = utils.timestamp_to_datetime(forward_header.date)

                if forward_header.from_id:
                    raw_peer_id = utils.get_raw_peer_id(forward_header.from_id)
                    peer_id = utils.get_peer_id(forward_header.from_id)

                    if peer_id > 0:
                        forward_from = types.User._parse(client, users[raw_peer_id])
                    else:
                        forward_from_chat = types.Chat._parse_channel_chat(client, chats[raw_peer_id])
                        forward_from_message_id = forward_header.channel_post
                        forward_signature = forward_header.post_author
                elif forward_header.from_name:
                    forward_sender_name = forward_header.from_name

            photo = None
            location = None
            contact = None
            venue = None
            game = None
            giveaway = None
            giveaway_result = None
            story = None
            audio = None
            voice = None
            animation = None
            video = None
            video_note = None
            web_page_preview = None
            sticker = None
            document = None
            poll = None
            dice = None

            media = message.media
            media_type = None
            has_media_spoiler = None

            if media:
                if isinstance(media, raw.types.MessageMediaPhoto):
                    photo = types.Photo._parse(client, media.photo, media.ttl_seconds)
                    media_type = enums.MessageMediaType.PHOTO
                    has_media_spoiler = media.spoiler
                elif isinstance(media, raw.types.MessageMediaGeo):
                    location = types.Location._parse(client, media.geo)
                    media_type = enums.MessageMediaType.LOCATION
                elif isinstance(media, raw.types.MessageMediaContact):
                    contact = types.Contact._parse(client, media)
                    media_type = enums.MessageMediaType.CONTACT
                elif isinstance(media, raw.types.MessageMediaVenue):
                    venue = types.Venue._parse(client, media)
                    media_type = enums.MessageMediaType.VENUE
                elif isinstance(media, raw.types.MessageMediaGame):
                    game = types.Game._parse(client, message)
                    media_type = enums.MessageMediaType.GAME
                elif isinstance(media, raw.types.MessageMediaGiveaway):
                    giveaway = await types.Giveaway._parse(client, message)
                    media_type = enums.MessageMediaType.GIVEAWAY
                elif isinstance(media, raw.types.MessageMediaGiveawayResults):
                    giveaway_result = await types.GiveawayResult._parse(client, message.media)
                    media_type = enums.MessageMediaType.GIVEAWAY_RESULT
                elif isinstance(media, raw.types.MessageMediaStory):
                    story = await types.MessageStory._parse(client, media)
                    media_type = enums.MessageMediaType.STORY
                elif isinstance(media, raw.types.MessageMediaDocument):
                    doc = media.document

                    if isinstance(doc, raw.types.Document):
                        attributes = {type(i): i for i in doc.attributes}

                        file_name = getattr(
                            attributes.get(
                                raw.types.DocumentAttributeFilename, None
                            ), "file_name", None
                        )

                        if raw.types.DocumentAttributeAnimated in attributes:
                            video_attributes = attributes.get(raw.types.DocumentAttributeVideo, None)
                            animation = types.Animation._parse(client, doc, video_attributes, file_name)
                            media_type = enums.MessageMediaType.ANIMATION
                            has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeSticker in attributes:
                            sticker = await types.Sticker._parse(client, doc, attributes)
                            media_type = enums.MessageMediaType.STICKER
                        elif raw.types.DocumentAttributeVideo in attributes:
                            video_attributes = attributes[raw.types.DocumentAttributeVideo]

                            if video_attributes.round_message:
                                video_note = types.VideoNote._parse(client, doc, video_attributes)
                                media_type = enums.MessageMediaType.VIDEO_NOTE
                            else:
                                video = types.Video._parse(client, doc, video_attributes, file_name, media.ttl_seconds)
                                media_type = enums.MessageMediaType.VIDEO
                                has_media_spoiler = media.spoiler
                        elif raw.types.DocumentAttributeAudio in attributes:
                            audio_attributes = attributes[raw.types.DocumentAttributeAudio]

                            if audio_attributes.voice:
                                voice = types.Voice._parse(client, doc, audio_attributes)
                                media_type = enums.MessageMediaType.VOICE
                            else:
                                audio = types.Audio._parse(client, doc, audio_attributes, file_name)
                                media_type = enums.MessageMediaType.AUDIO
                        else:
                            document = types.Document._parse(client, doc, file_name)
                            media_type = enums.MessageMediaType.DOCUMENT
                elif isinstance(media, raw.types.MessageMediaPoll):
                    poll = types.Poll._parse(client, media)
                    media_type = enums.MessageMediaType.POLL
                elif isinstance(media, raw.types.MessageMediaDice):
                    dice = types.Dice._parse(client, media)
                    media_type = enums.MessageMediaType.DICE
                else:
                    media = None

            reply_markup = message.reply_markup

            if reply_markup:
                if isinstance(reply_markup, raw.types.ReplyKeyboardForceReply):
                    reply_markup = types.ForceReply.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardMarkup):
                    reply_markup = types.ReplyKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyInlineMarkup):
                    reply_markup = types.InlineKeyboardMarkup.read(reply_markup)
                elif isinstance(reply_markup, raw.types.ReplyKeyboardHide):
                    reply_markup = types.ReplyKeyboardRemove.read(reply_markup)
                else:
                    reply_markup = None

            from_user = types.User._parse(client, users.get(user_id, None))
            sender_chat = types.Chat._parse(client, message, users, chats, is_chat=False) if not from_user else None

            reactions = types.MessageReactions._parse(client, message.reactions)

            parsed_message = Message(
                id=message.id,
                message_thread_id=message_thread_id,
                date=utils.timestamp_to_datetime(message.date),
                chat=types.Chat._parse(client, message, users, chats, is_chat=True),
                topics=None,
                from_user=from_user,
                sender_chat=sender_chat,
                text=(
                    Str(message.message).init(entities) or None
                    if media is None or web_page_preview is not None
                    else None
                ),
                caption=(
                    Str(message.message).init(entities) or None
                    if media is not None and web_page_preview is None
                    else None
                ),
                entities=(
                    entities or None
                    if media is None or web_page_preview is not None
                    else None
                ),
                caption_entities=(
                    entities or None
                    if media is not None and web_page_preview is None
                    else None
                ),
                author_signature=message.post_author,
                has_protected_content=message.noforwards,
                has_media_spoiler=has_media_spoiler,
                forward_from=forward_from,
                forward_sender_name=forward_sender_name,
                forward_from_chat=forward_from_chat,
                forward_from_message_id=forward_from_message_id,
                forward_signature=forward_signature,
                forward_date=forward_date,
                is_topic_message=is_topic_message,
                mentioned=message.mentioned,
                scheduled=is_scheduled,
                from_scheduled=message.from_scheduled,
                media=media_type,
                edit_hide=message.edit_hide,
                edit_date=utils.timestamp_to_datetime(message.edit_date),
                media_group_id=message.grouped_id,
                invert_media=message.invert_media,
                photo=photo,
                location=location,
                contact=contact,
                venue=venue,
                audio=audio,
                voice=voice,
                animation=animation,
                game=game,
                giveaway=giveaway,
                giveaway_result=giveaway_result,
                story=story,
                video=video,
                video_note=video_note,
                web_page_preview=web_page_preview,
                sticker=sticker,
                document=document,
                poll=poll,
                dice=dice,
                views=message.views,
                forwards=message.forwards,
                via_bot=types.User._parse(client, users.get(message.via_bot_id, None)),
                outgoing=message.out,
                reply_markup=reply_markup,
                reactions=reactions,
                effect_id=getattr(message, "effect", None),
                raw=message,
                client=client
            )

            if message.reply_to:
                if isinstance(message.reply_to, raw.types.MessageReplyHeader):
                    parsed_message.quote_text = message.reply_to.quote_text
                    if len(message.reply_to.quote_entities) > 0:
                        quote_entities = [types.MessageEntity._parse(client, entity, users) for entity in message.reply_to.quote_entities]
                        parsed_message.quote_entities = types.List(filter(lambda x: x is not None, quote_entities))
                    if message.reply_to.forum_topic:
                        if message.reply_to.reply_to_top_id:
                            thread_id = message.reply_to.reply_to_top_id
                            parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        else:
                            thread_id = message.reply_to.reply_to_msg_id
                        parsed_message.message_thread_id = thread_id
                        parsed_message.is_topic_message = True
                        if topics:
                            parsed_message.topics = types.ForumTopic._parse(topics[thread_id])
                        else:
                            try:
                                msg = await client.get_messages(parsed_message.chat.id,message.id)
                                if getattr(msg, "topics"):
                                    parsed_message.topics = msg.topics
                            except Exception:
                                pass
                    else:
                        parsed_message.reply_to_message_id = message.reply_to.reply_to_msg_id
                        parsed_message.reply_to_top_message_id = message.reply_to.reply_to_top_id
                else:
                    parsed_message.reply_to_story_id = message.reply_to.story_id
                    if isinstance(message.reply_to.peer, raw.types.PeerUser):
                        parsed_message.reply_to_story_user_id = message.reply_to.peer.user_id
                    elif isinstance(message.reply_to.peer, raw.types.PeerChat):
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.chat_id)
                    else:
                        parsed_message.reply_to_story_chat_id = utils.get_channel_id(message.reply_to.peer.channel_id)

                if replies:
                    if parsed_message.reply_to_message_id:
                        is_cross_chat = getattr(message.reply_to, "reply_to_peer_id", None) and getattr(message.reply_to.reply_to_peer_id, "channel_id", None)

                        if is_cross_chat:
                            key = (utils.get_channel_id(message.reply_to.reply_to_peer_id.channel_id), message.reply_to.reply_to_msg_id)
                            reply_to_params = {"chat_id": key[0], 'message_ids': key[1]}
                        else:
                            key = (parsed_message.chat.id, parsed_message.reply_to_message_id)
                            reply_to_params = {'chat_id': key[0], 'reply_to_message_ids': message.id}

                        try:
                            reply_to_message = client.message_cache[key]

                            if not reply_to_message:
                                reply_to_message = await client.get_messages(
                                    replies=replies - 1,
                                    **reply_to_params
                                )
                            if reply_to_message and not reply_to_message.forum_topic_created:
                                parsed_message.reply_to_message = reply_to_message
                        except MessageIdsEmpty:
                            pass
                        except ChannelPrivate:
                            pass
                    elif parsed_message.reply_to_story_id:
                        try:
                            reply_to_story = await client.get_stories(
                                parsed_message.reply_to_story_user_id or parsed_message.reply_to_story_chat_id,
                                parsed_message.reply_to_story_id
                            )
                        except Exception:
                            pass
                        else:
                            parsed_message.reply_to_story = reply_to_story

            if not parsed_message.poll:
                client.message_cache[(parsed_message.chat.id, parsed_message.id)] = parsed_message

            return parsed_message

    @property
    def link(self) -> str:
        if (
            self.chat.type in (enums.ChatType.GROUP, enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)
            and self.chat.username
        ):
            return f"https://t.me/{self.chat.username}/{self.id}"
        else:
            return f"https://t.me/c/{utils.get_channel_id(self.chat.id)}/{self.id}"

    async def get_media_group(self) -> List["types.Message"]:
        return await self._client.get_media_group(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def reply_text(
        self,
        text: str,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        message_effect_id: int = None,
        invert_media: bool = None,
        reply_markup=None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            message_effect_id=message_effect_id,
            invert_media=invert_media,
            reply_markup=reply_markup
        )

    reply = reply_text

    async def reply_animation(
        self,
        animation: Union[str, BinaryIO],
        quote: bool = None,
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
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_animation(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_audio(
        self,
        audio: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        performer: str = None,
        title: str = None,
        thumb: Union[str, BinaryIO] = None,
        file_name: str = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_audio(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_cached_media(
        self,
        file_id: str,
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_cached_media(
            chat_id=chat_id,
            file_id=file_id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup
        )

    async def reply_chat_action(
        self,
        action: "enums.ChatAction",
        emoji: str = None,
        emoji_message_id: int = None,
        emoji_message_interaction: "raw.types.DataJSON" = None
    ) -> bool:
        return await self._client.send_chat_action(
            chat_id=self.chat.id,
            action=action,
            emoji=emoji,
            emoji_message_id=emoji_message_id,
            emoji_message_interaction=emoji_message_interaction
        )

    async def reply_contact(
        self,
        phone_number: str,
        first_name: str,
        quote: bool = None,
        last_name: str = "",
        vcard: str = "",
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_contact(
            chat_id=chat_id,
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            vcard=vcard,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

    async def reply_document(
        self,
        document: Union[str, BinaryIO],
        quote: bool = None,
        thumb: Union[str, BinaryIO] = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        file_name: str = None,
        force_document: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_document(
            chat_id=chat_id,
            document=document,
            thumb=thumb,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            file_name=file_name,
            force_document=force_document,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_game(
        self,
        game_short_name: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        return await self._client.send_game(
            chat_id=self.chat.id,
            game_short_name=game_short_name,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

    async def reply_inline_bot_result(
        self,
        query_id: int,
        result_id: str,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        return await self._client.send_inline_bot_result(
            chat_id=self.chat.id,
            query_id=query_id,
            result_id=result_id,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            quote_text=quote_text
        )

    async def reply_location(
        self,
        latitude: float,
        longitude: float,
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_location(
            chat_id=chat_id,
            latitude=latitude,
            longitude=longitude,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
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
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        invert_media: bool = None
    ) -> List["types.Message"]:
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_media_group(
            chat_id=chat_id,
            media=media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            invert_media=invert_media
        )

    async def reply_photo(
        self,
        photo: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        ttl_seconds: int = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        view_once: bool = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_photo(
            chat_id=chat_id,
            photo=photo,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            has_spoiler=has_spoiler,
            ttl_seconds=ttl_seconds,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            view_once=view_once,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_sticker(
        self,
        sticker: Union[str, BinaryIO],
        quote: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_sticker(
            chat_id=chat_id,
            sticker=sticker,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video(
        self,
        video: Union[str, BinaryIO],
        quote: bool = None,
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
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_video(
            chat_id=chat_id,
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
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            invert_media=invert_media,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_video_note(
        self,
        video_note: Union[str, BinaryIO],
        quote: bool = None,
        duration: int = 0,
        length: int = 1,
        thumb: Union[str, BinaryIO] = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        protect_content: bool = None,
        ttl_seconds: int = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_video_note(
            chat_id=chat_id,
            video_note=video_note,
            duration=duration,
            length=length,
            thumb=thumb,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            protect_content=protect_content,
            ttl_seconds=ttl_seconds,
            parse_mode=parse_mode,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )

    async def reply_voice(
        self,
        voice: Union[str, BinaryIO],
        quote: bool = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        duration: int = 0,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = None,
        progress: Callable = None,
        progress_args: tuple = ()
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_voice(
            chat_id=chat_id,
            voice=voice,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            duration=duration,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            reply_markup=reply_markup,
            progress=progress,
            progress_args=progress_args
        )
    async def reply_web_page(
        self,
        url: str,
        text: str = "",
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        large_media: bool = None,
        invert_media: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_in_chat_id: Union[int, str] = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        reply_markup=None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != enums.ChatType.PRIVATE

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        message_thread_id = None
        if self.message_thread_id:
            message_thread_id = self.message_thread_id

        chat_id = self.chat.id
        reply_to_chat_id = None
        if reply_in_chat_id is not None:
            chat_id = reply_in_chat_id
            reply_to_chat_id = self.chat.id

        return await self._client.send_web_page(
            chat_id=chat_id,
            url=url,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            large_media=large_media,
            invert_media=invert_media,
            disable_notification=disable_notification,
            message_thread_id=message_thread_id,
            reply_to_message_id=reply_to_message_id,
            reply_to_chat_id=reply_to_chat_id,
            quote_text=quote_text,
            quote_entities=quote_entities,
            schedule_date=schedule_date,
            protect_content=protect_content,
            reply_markup=reply_markup
        )

    async def edit_text(
        self,
        text: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        return await self._client.edit_message_text(
            chat_id=self.chat.id,
            message_id=self.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            invert_media=invert_media,
            reply_markup=reply_markup
        )

    edit = edit_text

    async def edit_caption(
        self,
        caption: str,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        return await self._client.edit_message_caption(
            chat_id=self.chat.id,
            message_id=self.id,
            caption=caption,
            parse_mode=parse_mode,
            caption_entities=caption_entities,
            invert_media=invert_media,
            reply_markup=reply_markup
        )

    async def edit_media(
        self,
        media: "types.InputMedia",
        parse_mode: Optional["enums.ParseMode"] = None,
        invert_media: bool = None,
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> "Message":
        return await self._client.edit_message_media(
            chat_id=self.chat.id,
            message_id=self.id,
            media=media,
            parse_mode=parse_mode,
            invert_media=invert_media,
            reply_markup=reply_markup
        )

    async def edit_reply_markup(self, reply_markup: "types.InlineKeyboardMarkup" = None) -> "Message":
        return await self._client.edit_message_reply_markup(
            chat_id=self.chat.id,
            message_id=self.id,
            reply_markup=reply_markup
        )

    async def forward(
        self,
        chat_id: Union[int, str],
        message_thread_id: int = None,
        disable_notification: bool = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        drop_author: bool = None
    ) -> Union["types.Message", List["types.Message"]]:
        return await self._client.forward_messages(
            chat_id=chat_id,
            from_chat_id=self.chat.id,
            message_ids=self.id,
            message_thread_id=message_thread_id,
            disable_notification=disable_notification,
            schedule_date=schedule_date,
            protect_content=protect_content,
            drop_author=drop_author
        )

    async def copy(
        self,
        chat_id: Union[int, str],
        caption: str = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        has_spoiler: bool = None,
        disable_notification: bool = None,
        message_thread_id: int = None,
        quote_text: str = None,
        quote_entities: List["types.MessageEntity"] = None,
        reply_to_message_id: int = None,
        schedule_date: datetime = None,
        protect_content: bool = None,
        invert_media: bool = None,
        reply_markup: Union[
            "types.InlineKeyboardMarkup",
            "types.ReplyKeyboardMarkup",
            "types.ReplyKeyboardRemove",
            "types.ForceReply"
        ] = object
    ) -> Union["types.Message", List["types.Message"]]:
        if self.service:
            log.warning("Service messages cannot be copied. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.game and not await self._client.storage.is_bot():
            log.warning("Users cannot send messages with Game media type. chat_id: %s, message_id: %s",
                        self.chat.id, self.id)
        elif self.empty:
            log.warning("Empty messages cannot be copied.")
        elif self.text:
            return await self._client.send_message(
                chat_id,
                text=self.text,
                entities=self.entities,
                parse_mode=enums.ParseMode.DISABLED,
                disable_web_page_preview=not self.web_page_preview,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                quote_text=quote_text,
            quote_entities=quote_entities,
                schedule_date=schedule_date,
                protect_content=protect_content,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )
        elif self.media:
            send_media = partial(
                self._client.send_cached_media,
                chat_id=chat_id,
                disable_notification=disable_notification,
                message_thread_id=message_thread_id,
                reply_to_message_id=reply_to_message_id,
                schedule_date=schedule_date,
                has_spoiler=has_spoiler,
                protect_content=protect_content,
                invert_media=invert_media,
                reply_markup=self.reply_markup if reply_markup is object else reply_markup
            )

            if self.photo:
                file_id = self.photo.file_id
            elif self.audio:
                file_id = self.audio.file_id
            elif self.document:
                file_id = self.document.file_id
            elif self.video:
                file_id = self.video.file_id
            elif self.animation:
                file_id = self.animation.file_id
            elif self.voice:
                file_id = self.voice.file_id
            elif self.sticker:
                file_id = self.sticker.file_id
            elif self.video_note:
                file_id = self.video_note.file_id
            elif self.contact:
                return await self._client.send_contact(
                    chat_id,
                    phone_number=self.contact.phone_number,
                    first_name=self.contact.first_name,
                    last_name=self.contact.last_name,
                    vcard=self.contact.vcard,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
            elif self.location:
                return await self._client.send_location(
                    chat_id,
                    latitude=self.location.latitude,
                    longitude=self.location.longitude,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    schedule_date=schedule_date
                )
            elif self.web_page_preview:
                return await self._client.send_web_page(
                    chat_id,
                    url=self.web_page_preview.webpage.url,
                    text=self.text,
                    entities=self.entities,
                    parse_mode=enums.ParseMode.DISABLED,
                    large_media=self.web_page_preview.force_large_media,
                    invert_media=self.web_page_preview.invert_media,
                    disable_notification=disable_notification,
                    message_thread_id=message_thread_id,
                    reply_to_message_id=reply_to_message_id,
                    quote_text=quote_text,
                    quote_entities=quote_entities,
                    schedule_date=schedule_date,
                    protect_content=protect_content,
                    reply_markup=self.reply_markup if reply_markup is object else reply_markup
                )
            else:
                raise ValueError("Unknown media type")

            if self.sticker or self.video_note:
                return await send_media(
                    file_id=file_id,
                    message_thread_id=message_thread_id
                )
            else:
                if caption is None:
                    caption = self.caption or ""
                    caption_entities = self.caption_entities

                return await send_media(
                    file_id=file_id,
                    caption=caption,
                    parse_mode=parse_mode,
                    caption_entities=caption_entities,
                    has_spoiler=has_spoiler,
                    message_thread_id=message_thread_id
                )
        else:
            raise ValueError("Can't copy this message")

    async def delete(self, revoke: bool = True):
        return await self._client.delete_messages(
            chat_id=self.chat.id,
            message_ids=self.id,
            revoke=revoke
        )

    async def click(
        self,
        x: Union[int, str] = 0,
        y: int = None,
        quote: bool = None,
        timeout: int = 10,
        request_write_access: bool = True,
        password: str = None
    ):
        if isinstance(self.reply_markup, types.ReplyKeyboardMarkup):
            keyboard = self.reply_markup.keyboard
            is_inline = False
        elif isinstance(self.reply_markup, types.InlineKeyboardMarkup):
            keyboard = self.reply_markup.inline_keyboard
            is_inline = True
        else:
            raise ValueError("The message doesn't contain any keyboard")

        if isinstance(x, int) and y is None:
            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                ][x]
            except IndexError:
                raise ValueError(f"The button at index {x} doesn't exist")
        elif isinstance(x, int) and isinstance(y, int):
            try:
                button = keyboard[y][x]
            except IndexError:
                raise ValueError(f"The button at position ({x}, {y}) doesn't exist")
        elif isinstance(x, str) and y is None:
            label = x.encode("utf-16", "surrogatepass").decode("utf-16")

            try:
                button = [
                    button
                    for row in keyboard
                    for button in row
                    if label == button.text
                ][0]
            except IndexError:
                raise ValueError(f"The button with label '{x}' doesn't exists")
        else:
            raise ValueError("Invalid arguments")

        if is_inline:
            if button.callback_data:
                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    timeout=timeout
                )
            elif button.requires_password:
                if password is None:
                    raise ValueError(
                        "This button requires a password"
                    )

                return await self._client.request_callback_answer(
                    chat_id=self.chat.id,
                    message_id=self.id,
                    callback_data=button.callback_data,
                    password=password,
                    timeout=timeout
                )
            elif button.url:
                return button.url
            elif button.web_app:
                web_app = button.web_app

                bot_peer_id = (
                    self.via_bot and
                    self.via_bot.id
                ) or (
                    self.from_user and
                    self.from_user.is_bot and
                    self.from_user.id
                ) or None

                if not bot_peer_id:
                    raise ValueError(
                        "This button requires a bot as the sender"
                    )

                r = await self._client.invoke(
                    raw.functions.messages.RequestWebView(
                        peer=await self._client.resolve_peer(self.chat.id),
                        bot=await self._client.resolve_peer(bot_peer_id),
                        url=web_app.url,
                        platform=self._client.client_platform.value,
                        # TODO
                    )
                )
                return r.url
            elif button.user_id:
                return await self._client.get_chat(
                    button.user_id,
                    force_full=False
                )
            elif button.switch_inline_query:
                return button.switch_inline_query
            elif button.switch_inline_query_current_chat:
                return button.switch_inline_query_current_chat
            else:
                raise ValueError("This button is not supported yet")
        else:
            await self.reply(text=button, quote=quote)

    async def react(self, emoji: str = "", big: bool = False, add_to_recent: bool = True) -> "types.MessageReactions":
        return await self._client.send_reaction(
            chat_id=self.chat.id,
            message_id=self.id,
            emoji=emoji,
            big=big
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

    async def pin(self, disable_notification: bool = False, both_sides: bool = False) -> "types.Message":
        return await self._client.pin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id,
            disable_notification=disable_notification,
            both_sides=both_sides
        )

    async def unpin(self) -> bool:
        return await self._client.unpin_chat_message(
            chat_id=self.chat.id,
            message_id=self.id
        )

    async def ask(
        self,
        text: str,
        quote: bool = None,
        parse_mode: Optional["enums.ParseMode"] = None,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None,
        disable_notification: bool = None,
        reply_to_message_id: int = None,
        reply_markup=None,
        filters=None,
        timeout: int = None
    ) -> "Message":
        if quote is None:
            quote = self.chat.type != "private"

        if reply_to_message_id is None and quote:
            reply_to_message_id = self.id

        request = await self._client.send_message(
            chat_id=self.chat.id,
            text=text,
            parse_mode=parse_mode,
            entities=entities,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            reply_to_message_id=reply_to_message_id,
            reply_markup=reply_markup
        )

        reply_message = await self._client.wait_for_message(
            self.chat.id,
            filters=filters,
            timeout=timeout
        )

        reply_message.request = request
        return reply_message
