from __future__ import annotations

methods_all = {
    "utilities": """
        Utilities
            start
            stop
            run
            run_sync
            restart
            add_handler
            remove_handler
            stop_transmission
            export_session_string
            set_parse_mode
        """,
    "messages": """
        Messages
            send_message
            forward_messages
            copy_message
            copy_media_group
            send_photo
            send_audio
            send_document
            send_sticker
            send_video
            send_animation
            send_voice
            send_video_note
            send_web_page
            send_media_group
            send_location
            send_venue
            send_contact
            send_cached_media
            send_reaction
            edit_message_text
            edit_message_caption
            edit_message_media
            edit_message_reply_markup
            edit_inline_text
            edit_inline_caption
            edit_inline_media
            edit_inline_reply_markup
            send_chat_action
            delete_messages
            delete_scheduled_messages
            get_available_effects
            get_messages
            get_scheduled_messages
            get_media_group
            get_chat_history
            get_chat_history_count
            read_chat_history
            send_poll
            vote_poll
            stop_poll
            retract_vote
            send_dice
            search_messages
            search_messages_count
            search_global
            search_global_count
            search_global_hashtag_messages
            search_global_hashtag_messages_count
            download_media
            stream_media
            get_discussion_message
            get_discussion_replies
            get_discussion_replies_count
            get_custom_emoji_stickers
        """,
    "chats": """
        Chats
            join_chat
            leave_chat
            ban_chat_member
            unban_chat_member
            restrict_chat_member
            promote_chat_member
            set_administrator_title
            set_chat_photo
            delete_chat_photo
            delete_folder
            export_folder_link
            update_folder
            set_chat_title
            set_chat_description
            set_chat_permissions
            pin_chat_message
            unpin_chat_message
            unpin_all_chat_messages
            get_chat
            get_chat_member
            get_chat_members
            get_chat_members_count
            get_dialogs
            get_dialogs_count
            get_folders
            get_forum_topics
            get_forum_topics_by_id
            set_chat_username
            get_nearby_chats
            archive_chats
            unarchive_chats
            add_chat_members
            create_channel
            create_group
            create_supergroup
            delete_channel
            delete_supergroup
            delete_user_history
            set_slow_mode
            mark_chat_unread
            get_chat_event_log
            get_chat_online_count
            get_send_as_chats
            set_send_as_chat
            set_chat_protected_content
            close_forum_topic
            close_general_topic
            create_forum_topic
            delete_forum_topic
            edit_forum_topic
            edit_general_topic
            hide_general_topic
            reopen_forum_topic
            reopen_general_topic
            unhide_general_topic
            update_color
            delete_chat_history
            update_folder
        """,
    "users": """
        Users
            get_me
            get_users
            get_chat_photos
            get_chat_photos_count
            set_profile_photo
            delete_profile_photos
            set_username
            update_birthday
            update_personal_chat
            update_profile
            block_user
            unblock_user
            get_common_chats
            get_default_emoji_statuses
            set_emoji_status
        """,
    "stories": """
        Stories
            delete_stories
            edit_story
            export_story_link
            forward_story
            get_all_stories
            get_stories
            get_stories_history
            get_peer_stories
            send_story
        """,
    "stickers": """
        Stickers
            add_sticker_to_set
            create_sticker_set
            get_sticker_set
        """,
    "invite_links": """
        Invite Links
            get_chat_invite_link
            export_chat_invite_link
            create_chat_invite_link
            edit_chat_invite_link
            revoke_chat_invite_link
            delete_chat_invite_link
            get_chat_invite_link_joiners
            get_chat_invite_link_joiners_count
            get_chat_admin_invite_links
            get_chat_admin_invite_links_count
            get_chat_admins_with_invite_links
            get_chat_join_requests
            delete_chat_admin_invite_links
            approve_chat_join_request
            approve_all_chat_join_requests
            decline_chat_join_request
            decline_all_chat_join_requests
        """,
    "contacts": """
        Contacts
            add_contact
            delete_contacts
            import_contacts
            get_contacts
            get_contacts_count
            search_contacts
        """,
    "password": """
        Password
            enable_cloud_password
            change_cloud_password
            remove_cloud_password
        """,
    "bots": """
        Bots
            get_inline_bot_results
            send_inline_bot_result
            answer_callback_query
            answer_inline_query
            request_callback_answer
            send_game
            set_game_score
            get_game_high_scores
            set_bot_commands
            get_bot_commands
            delete_bot_commands
            set_bot_default_privileges
            get_bot_default_privileges
            set_chat_menu_button
            get_chat_menu_button
            answer_web_app_query
            get_bot_info
            set_bot_info
            get_collectible_item_info
        """,
    "business": """
        Telegram Business
            answer_pre_checkout_query
            answer_shipping_query
            create_invoice_link
            get_business_connection
            get_stars_transactions
            get_stars_transactions_by_id
            refund_star_payment
            send_invoice
            send_paid_media
        """,
    "authorization": """
        Authorization
            connect
            disconnect
            initialize
            terminate
            send_code
            resend_code
            sign_in
            sign_in_bot
            sign_up
            get_password_hint
            check_password
            send_recovery_code
            recover_password
            accept_terms_of_service
            log_out
            get_active_sessions
            reset_session
            reset_sessions
        """,
    "advanced": """
        Advanced
            invoke
            resolve_peer
            save_file
        """,
    "account": """
        Account
            get_account_ttl
            set_account_ttl
            set_privacy
            get_privacy
        """,
}

types_all = {
    "users_chats": """
        Users & Chats
            Birthday
            BusinessInfo
            BusinessMessage
            BusinessRecipients
            BusinessSchedule
            BusinessWeeklyOpen
            BusinessWorkingHours
            User
            Chat
            ChatPreview
            ChatPhoto
            ChatMember
            ChatPermissions
            ChatPrivileges
            ChatInviteLink
            ChatAdminWithInviteLinks
            ChatEvent
            ChatEventFilter
            ChatMemberUpdated
            ChatJoinRequest
            ChatJoinedByRequest
            ChatJoiner
            Dialog
            Folder
            Restriction
            EmojiStatus
            ForumTopic
            PeerUser
            PeerChannel
            BotInfo
            ChatColor
            FoundContacts
            PrivacyRule
            CollectibleItemInfo
        """,
    "messages_media": """
        Messages & Media
            Message
            MessageEntity
            Photo
            Thumbnail
            Audio
            AvailableEffect
            Document
            Animation
            LabeledPrice
            Video
            Voice
            VideoNote
            Contact
            Location
            Venue
            Sticker
            StickerSet
            ContactRegistered
            ScreenshotTaken
            Game
            GiftedPremium
            Giveaway
            GiveawayLaunched
            GiveawayResult
            MessageStory
            WebPage
            WebPageEmpty
            WebPagePreview
            Poll
            PollOption
            Dice
            Reaction
            VideoChatScheduled
            VideoChatStarted
            VideoChatEnded
            VideoChatMembersInvited
            WebAppData
            MessageReactions
            ChatReactions
            ForumTopicCreated
            ForumTopicEdited
            ForumTopicClosed
            ForumTopicReopened
            GeneralTopicHidden
            GeneralTopicUnhidden
            Reaction
            ReactionCount
            ReactionType
            MessageReactionUpdated
            MessageReactionCountUpdated
        """,
    "stories": """
        Stories
            Story
            StoryDeleted
            StoryForwardHeader
            StorySkipped
            StoriesPrivacyRules
            StoryViews
            MediaArea
            MediaAreaChannelPost
            MediaAreaCoordinates
            InputMediaArea
            InputMediaAreaChannelPost
        """,
    "bot": """
        Bot
            BotAllowed
            BotApp
            BotBusinessConnection
        """,
    "bot_keyboards": """
        Bot keyboards
            ReplyKeyboardMarkup
            KeyboardButton
            ReplyKeyboardRemove
            InlineKeyboardMarkup
            InlineKeyboardButton
            InlineKeyboardButtonBuy
            RequestPeerTypeChannel
            RequestPeerTypeChat
            RequestPeerTypeUser
            RequestedChats
            RequestedChat
            RequestedUser
            LoginUrl
            ForceReply
            CallbackQuery
            GameHighScore
            CallbackGame
            WebAppInfo
            MenuButton
            MenuButtonCommands
            MenuButtonWebApp
            MenuButtonDefault
            SentWebAppMessage
            PreCheckoutQuery
        """,
    "bot_commands": """
        Bot commands
            BotCommand
            BotCommandScope
            BotCommandScopeDefault
            BotCommandScopeAllPrivateChats
            BotCommandScopeAllGroupChats
            BotCommandScopeAllChatAdministrators
            BotCommandScopeChat
            BotCommandScopeChatAdministrators
            BotCommandScopeChatMember
        """,
    "business": """
        Telegram Business
            ExtendedMediaPreview
            InputStarsTransaction
            Invoice
            PaidMedia
            PaidMediaPreview
            PaymentInfo
            PaymentRefunded
            ShippingAddress
            ShippingOption
            ShippingQuery
            StarsStatus
            StarsTransaction
            SuccessfulPayment
        """,
    "input_media": """
        Input Media
            InputMedia
            InputMediaPhoto
            InputMediaVideo
            InputMediaAudio
            InputMediaAnimation
            InputMediaDocument
            InputPhoneContact
        """,
    "inline_mode": """
        Inline Mode
            InlineQuery
            InlineQueryResult
            InlineQueryResultCachedAudio
            InlineQueryResultCachedDocument
            InlineQueryResultCachedAnimation
            InlineQueryResultCachedPhoto
            InlineQueryResultCachedSticker
            InlineQueryResultCachedVideo
            InlineQueryResultCachedVoice
            InlineQueryResultArticle
            InlineQueryResultAudio
            InlineQueryResultContact
            InlineQueryResultDocument
            InlineQueryResultAnimation
            InlineQueryResultLocation
            InlineQueryResultPhoto
            InlineQueryResultVenue
            InlineQueryResultVideo
            InlineQueryResultVoice
            ChosenInlineResult
        """,
    "pre_checkout_query": """
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
    "shipping_query": """
        ShippingQuery
            ShippingQuery.answer
        """,
    "input_message_content": """
        InputMessageContent
            InputMessageContent
            InputReplyToMessage
            InputReplyToStory
            InputTextMessageContent
            InputLocationMessageContent
            InputVenueMessageContent
            InputContactMessageContent
            InputInvoiceMessageContent
        """,
    "authorization": """
        Authorization
            ActiveSession
            ActiveSessions
            SentCode
            TermsOfService
        """,
    "input_privacy_rule": """
        InputPrivacyRule
            InputPrivacyRuleAllowAll
            InputPrivacyRuleAllowContacts
            InputPrivacyRuleAllowPremium
            InputPrivacyRuleAllowUsers
            InputPrivacyRuleAllowChats
            InputPrivacyRuleDisallowAll
            InputPrivacyRuleDisallowContacts
            InputPrivacyRuleDisallowUsers
            InputPrivacyRuleDisallowChats
        """,
}

bounds_all = {
    "message": """
        Message
            Message.ask
            Message.click
            Message.delete
            Message.download
            Message.forward
            Message.copy
            Message.pin
            Message.unpin
            Message.edit
            Message.edit_text
            Message.edit_caption
            Message.edit_media
            Message.edit_reply_markup
            Message.reply
            Message.reply_text
            Message.reply_animation
            Message.reply_audio
            Message.reply_cached_media
            Message.reply_chat_action
            Message.reply_contact
            Message.reply_document
            Message.reply_game
            Message.reply_inline_bot_result
            Message.reply_location
            Message.reply_media_group
            Message.reply_photo
            Message.reply_poll
            Message.reply_sticker
            Message.reply_venue
            Message.reply_video
            Message.reply_video_note
            Message.reply_voice
            Message.reply_web_page
            Message.get_media_group
            Message.react
            Message.wait_for_click
        """,
    "chat": """
        Chat
            Chat.ask
            Chat.listen
            Chat.stop_listening
            Chat.archive
            Chat.unarchive
            Chat.set_title
            Chat.set_description
            Chat.set_photo
            Chat.ban_member
            Chat.unban_member
            Chat.restrict_member
            Chat.promote_member
            Chat.get_member
            Chat.get_members
            Chat.add_members
            Chat.join
            Chat.leave
            Chat.mark_unread
            Chat.set_protected_content
            Chat.unpin_all_messages
        """,
    "user": """
        User
            User.ask
            User.listen
            User.stop_listening
            User.archive
            User.unarchive
            User.block
            User.unblock
        """,
    "story": """
        Story
            Story.delete
            Story.download
            Story.edit
            Story.edit_animation
            Story.edit_caption
            Story.edit_photo
            Story.edit_privacy
            Story.edit_video
            Story.export_link
            Story.forward
            Story.reply_text
            Story.reply_animation
            Story.reply_audio
            Story.reply_cached_media
            Story.reply_media_group
            Story.reply_photo
            Story.reply_sticker
            Story.reply_video
            Story.reply_video_note
            Story.reply_voice
        """,
    "callback_query": """
        Callback Query
            CallbackQuery.answer
            CallbackQuery.edit_message_text
            CallbackQuery.edit_message_caption
            CallbackQuery.edit_message_media
            CallbackQuery.edit_message_reply_markup
        """,
    "inline_query": """
        InlineQuery
            InlineQuery.answer
        """,
    "pre_checkout_query": """
        PreCheckoutQuery
            PreCheckoutQuery.answer
        """,
    "shipping_query": """
        ShippingQuery
            ShippingQuery.answer
        """,
    "chat_join_request": """
        ChatJoinRequest
            ChatJoinRequest.approve
            ChatJoinRequest.decline
        """,
}


from __future__ import annotations

import ast
import os
import re
import shutil

# Constants
HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
PYROGRAM_API_DEST = "docs/source/api"
FUNCTIONS_PATH = "pyrogram/raw/functions"
TYPES_PATH = "pyrogram/raw/types"
BASE_PATH = "pyrogram/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snek(s: str) -> str:
    """Convert CamelCase to snake_case."""
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path: str, base: str):
    """Generate documentation for the given source path."""
    all_entities = {}

    def build(path: str, level: int = 0):
        last = os.path.basename(path)

        for item in os.listdir(path):
            full_item_path = os.path.join(path, item)
            if os.path.isdir(full_item_path) and not item.startswith("__"):
                build(full_item_path, level + 1)
            elif os.path.isfile(full_item_path):
                with open(full_item_path, encoding="utf-8") as f:
                    p = ast.parse(f.read())
                    name = next(
                        (
                            node.name
                            for node in ast.walk(p)
                            if isinstance(node, ast.ClassDef)
                        ),
                        None,
                    )

                if not name:
                    continue

                full_path = os.path.join(
                    base if level else "",
                    last,
                    snek(name).replace("_", "-") + ".rst",
                )

                namespace = last if last in ["base", "types", "functions"] else ""
                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                os.makedirs(
                    os.path.join(DESTINATION, os.path.dirname(full_path)),
                    exist_ok=True,
                )

                with open(
                    os.path.join(DESTINATION, full_path), "w", encoding="utf-8"
                ) as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path=f"pyrogram.raw.{'.'.join(full_path.split('/')[:-1])}.{name}",
                        )
                    )

                all_entities.setdefault(last, []).append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = [f'{i} <{snek(i).replace("_", "-")}>' for i in v]

        if k != base:
            inner_path = os.path.join(base, k, "index.rst")
            module = f"pyrogram.raw.{base}.{k}"
        else:
            for i in sorted(all_entities, reverse=True):
                if i != base:
                    entities.insert(0, f"{i}/index")

            inner_path = os.path.join(base, "index.rst")
            module = f"pyrogram.raw.{base}"

        with open(os.path.join(DESTINATION, inner_path), "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities),
                )
            )


def pyrogram_api():
    """Generate Pyrogram API documentation."""

    def get_title_list(s: str) -> list:
        return [line.strip() for line in s.split("\n") if line.strip()]

    def create_docs(root: str, template_path: str, items: dict, entity_type: str):
        """Create documentation for methods, types, or bound methods."""
        shutil.rmtree(root, ignore_errors=True)
        os.mkdir(root)

        with open(template_path) as f:
            template = f.read()

        with open(os.path.join(root, "index.rst"), "w") as f:
            fmt_keys = {}

            for k, v in items.items():
                name, *entities = get_title_list(v)
                fmt_keys[k] = "\n    ".join(f"{m} <{m}>" for m in entities)

                for entity in entities:
                    with open(os.path.join(root, f"{entity}.rst"), "w") as f2:
                        title = f"{entity}()"
                        f2.write(f"{title}\n{'=' * len(title)}\n\n")
                        f2.write(
                            f".. automethod:: pyrogram.{entity_type}.{entity}()"
                        )

            f.write(template.format(**fmt_keys))

    create_docs(
        os.path.join(PYROGRAM_API_DEST, "methods"),
        os.path.join(HOME, "template/methods.rst"),
        methods_all,
        "Client",
    )
    create_docs(
        os.path.join(PYROGRAM_API_DEST, "types"),
        os.path.join(HOME, "template/types.rst"),
        types_all,
        "types",
    )
    create_docs(
        os.path.join(PYROGRAM_API_DEST, "bound-methods"),
        os.path.join(HOME, "template/bound-methods.rst"),
        b_all,
        "types",
    )


def start():
    """Initialize the documentation generation process."""
    global page_template, toctree

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with open(os.path.join(HOME, "template/page.txt"), encoding="utf-8") as f:
        page_template = f.read()

    with open(os.path.join(HOME, "template/toctree.txt"), encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    pyrogram_api()


if __name__ == "__main__":
    FUNCTIONS_PATH = "../../pyrogram/raw/functions"
    TYPES_PATH = "../../pyrogram/raw/types"
    BASE_PATH = "../../pyrogram/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    PYROGRAM_API_DEST = "../../docs/source/api"

    start()
