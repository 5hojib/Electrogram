from __future__ import annotations

import asyncio
import base64
import functools
import hashlib
import os
import struct
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timezone
from getpass import getpass
from typing import TYPE_CHECKING, Any, TypeVar

import pyrogram
from pyrogram import enums, raw, types
from pyrogram.file_id import (
    DOCUMENT_TYPES,
    PHOTO_TYPES,
    FileId,
    FileType,
)

if TYPE_CHECKING:
    from collections.abc import Callable


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def get_input_media_from_file_id(
    file_id: str,
    expected_file_type: FileType = None,
    ttl_seconds: int | None = None,
) -> raw.types.InputMediaPhoto | raw.types.InputMediaDocument:
    try:
        decoded = FileId.decode(file_id)
    except Exception:
        raise ValueError(
            f'Failed to decode "{file_id}". The value does not represent an existing local file, '
            f"HTTP URL, or valid file id."
        )

    file_type = decoded.file_type

    if expected_file_type is not None and file_type != expected_file_type:
        raise ValueError(
            f"Expected {expected_file_type.name}, got {file_type.name} file id instead"
        )

    if file_type in (FileType.THUMBNAIL, FileType.CHAT_PHOTO):
        raise ValueError(f"This file id can only be used for download: {file_id}")

    if file_type in PHOTO_TYPES:
        return raw.types.InputMediaPhoto(
            id=raw.types.InputPhoto(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
            ),
            ttl_seconds=ttl_seconds,
        )

    if file_type in DOCUMENT_TYPES:
        return raw.types.InputMediaDocument(
            id=raw.types.InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference,
            ),
            ttl_seconds=ttl_seconds,
        )

    raise ValueError(f"Unknown file id: {file_id}")


async def parse_messages(
    client,
    messages: raw.types.messages.Messages,
    replies: int = 1,
    business_connection_id: str | None = None,
) -> list[types.Message]:
    users = {i.id: i for i in messages.users}
    chats = {i.id: i for i in messages.chats}
    if hasattr(messages, "topics"):
        topics = {i.id: i for i in messages.topics}
    else:
        topics = None
    if not messages.messages:
        return types.List()

    parsed_messages = [
        await types.Message._parse(
            client,
            message,
            users,
            chats,
            topics,
            replies=0,
            business_connection_id=business_connection_id,
        )
        for message in messages.messages
    ]

    if replies:
        messages_with_replies = {
            i.id: i.reply_to
            for i in messages.messages
            if not isinstance(i, raw.types.MessageEmpty)
            and i.reply_to
            and isinstance(i.reply_to, raw.types.MessageReplyHeader)
        }

        message_reply_to_story = {
            i.id: {
                "user_id": i.reply_to.user_id,
                "story_id": i.reply_to.story_id,
            }
            for i in messages.messages
            if not isinstance(i, raw.types.MessageEmpty)
            and i.reply_to
            and isinstance(i.reply_to, raw.types.MessageReplyStoryHeader)
        }

        if messages_with_replies:
            for m in parsed_messages:
                if not isinstance(m, types.Message):
                    continue

                if m.chat:
                    chat_id = m.chat.id
                    break
            else:
                chat_id = 0

            is_all_within_chat = not any(
                value.reply_to_peer_id for value in messages_with_replies.values()
            )
            reply_messages: list[pyrogram.types.Message] = []
            if is_all_within_chat:
                # fast path: fetch all messages within the same chat
                reply_messages = await client.get_messages(
                    chat_id,
                    reply_to_message_ids=messages_with_replies.keys(),
                    replies=replies - 1,
                )
            else:
                for target_reply_to in messages_with_replies.values():
                    to_be_added_msg = None
                    the_chat_id = chat_id
                    if target_reply_to.reply_to_peer_id:
                        the_chat_id = get_channel_id(
                            target_reply_to.reply_to_peer_id.channel_id
                        )
                    to_be_added_msg = await client.get_messages(
                        chat_id=the_chat_id,
                        message_ids=target_reply_to.reply_to_msg_id,
                        replies=replies - 1,
                    )
                    if isinstance(to_be_added_msg, list):
                        for current_to_be_added in to_be_added_msg:
                            reply_messages.append(current_to_be_added)
                    elif to_be_added_msg:
                        reply_messages.append(to_be_added_msg)

            for message in parsed_messages:
                reply_to = messages_with_replies.get(message.id, None)
                if not reply_to:
                    continue

                reply_id = reply_to.reply_to_msg_id

                for reply in reply_messages:
                    if reply.id == reply_id and not reply.forum_topic_created:
                        message.reply_to_message = reply

        if message_reply_to_story:
            for m in parsed_messages:
                if not isinstance(m, types.Message):
                    continue

                if m.chat:
                    chat_id = m.chat.id
                    break
            else:
                chat_id = 0

            reply_messages = {}
            for msg_id in message_reply_to_story:
                reply_messages[msg_id] = await client.get_stories(
                    message_reply_to_story[msg_id]["user_id"],
                    message_reply_to_story[msg_id]["story_id"],
                )

            for message in parsed_messages:
                if message.id in reply_messages:
                    message.reply_to_story = reply_messages[message.id]

    return types.List(parsed_messages)


def parse_deleted_messages(
    client, update, business_connection_id: str | None = None
) -> list[types.Message]:
    messages = update.messages
    channel_id = getattr(update, "channel_id", None)

    parsed_messages = [
        types.Message(
            id=message,
            chat=types.Chat(
                id=get_channel_id(channel_id),
                type=enums.ChatType.CHANNEL,
                client=client,
            )
            if channel_id is not None
            else None,
            business_connection_id=business_connection_id,
            client=client,
        )
        for message in messages
    ]

    return types.List(parsed_messages)


def pack_inline_message_id(
    msg_id: raw.base.InputBotInlineMessageID,
):
    if isinstance(msg_id, raw.types.InputBotInlineMessageID):
        inline_message_id_packed = struct.pack(
            "<iqq", msg_id.dc_id, msg_id.id, msg_id.access_hash
        )
    else:
        inline_message_id_packed = struct.pack(
            "<iqiq",
            msg_id.dc_id,
            msg_id.owner_id,
            msg_id.id,
            msg_id.access_hash,
        )

    return base64.urlsafe_b64encode(inline_message_id_packed).decode().rstrip("=")


def unpack_inline_message_id(
    inline_message_id: str,
) -> raw.base.InputBotInlineMessageID:
    padded = inline_message_id + "=" * (-len(inline_message_id) % 4)
    decoded = base64.urlsafe_b64decode(padded)

    if len(decoded) == 20:
        unpacked = struct.unpack("<iqq", decoded)

        return raw.types.InputBotInlineMessageID(
            dc_id=unpacked[0], id=unpacked[1], access_hash=unpacked[2]
        )
    unpacked = struct.unpack("<iqiq", decoded)

    return raw.types.InputBotInlineMessageID64(
        dc_id=unpacked[0],
        owner_id=unpacked[1],
        id=unpacked[2],
        access_hash=unpacked[3],
    )


MIN_CHANNEL_ID = -1007852516352
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -999999999999
MAX_USER_ID = 999999999999


def get_raw_peer_id(
    peer: raw.base.Peer | raw.base.RequestedPeer,
) -> int | None:
    """Get the raw peer id from a Peer object"""
    if isinstance(peer, raw.types.PeerUser | raw.types.RequestedPeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat | raw.types.RequestedPeerChat):
        return peer.chat_id

    if isinstance(peer, raw.types.PeerChannel | raw.types.RequestedPeerChannel):
        return peer.channel_id

    return None


def get_peer_id(peer: raw.base.Peer) -> int:
    """Get the non-raw peer id from a Peer object"""
    if isinstance(peer, raw.types.PeerUser):
        return peer.user_id

    if isinstance(peer, raw.types.PeerChat):
        return -peer.chat_id

    if isinstance(peer, raw.types.PeerChannel):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError(f"Peer type invalid: {peer}")


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if peer_id >= MIN_CHAT_ID:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id


def btoi(b: bytes) -> int:
    return int.from_bytes(b, "big")


def itob(i: int) -> bytes:
    return i.to_bytes(256, "big")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))


def compute_password_hash(
    algo: raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow,
    password: str,
) -> bytes:
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1)
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2)


def compute_password_check(
    r: raw.types.account.Password, password: str
) -> raw.types.InputCheckPasswordSRP:
    algo = r.current_algo

    p_bytes = algo.p
    p = btoi(algo.p)

    g_bytes = itob(algo.g)
    g = algo.g

    B_bytes = r.srp_B
    B = btoi(B_bytes)

    srp_id = r.srp_id

    x_bytes = compute_password_hash(algo, password)
    x = btoi(x_bytes)

    g_x = pow(g, x, p)

    k_bytes = sha256(p_bytes + g_bytes)
    k = btoi(k_bytes)

    kg_x = (k * g_x) % p

    while True:
        a_bytes = os.urandom(256)
        a = btoi(a_bytes)

        A = pow(g, a, p)
        A_bytes = itob(A)

        u = btoi(sha256(A_bytes + B_bytes))

        if u > 0:
            break

    g_b = (B - kg_x) % p

    ux = u * x
    a_ux = a + ux
    S = pow(g_b, a_ux, p)
    S_bytes = itob(S)

    K_bytes = sha256(S_bytes)

    M1_bytes = sha256(
        xor(sha256(p_bytes), sha256(g_bytes))
        + sha256(algo.salt1)
        + sha256(algo.salt2)
        + A_bytes
        + B_bytes
        + K_bytes
    )

    return raw.types.InputCheckPasswordSRP(srp_id=srp_id, A=A_bytes, M1=M1_bytes)


async def parse_text_entities(
    client: pyrogram.Client,
    text: str,
    parse_mode: enums.ParseMode,
    entities: list[types.MessageEntity],
) -> dict[str, str | list[raw.base.MessageEntity]]:
    if entities:
        for entity in entities:
            entity._client = client

        entities = [await entity.write() for entity in entities] or None
    else:
        text, entities = (await client.parser.parse(text, parse_mode)).values()

    return {"message": text, "entities": entities}


def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def timestamp_to_datetime(ts: int | None) -> datetime | None:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: datetime | None) -> int | None:
    return int(dt.timestamp()) if dt else None


async def run_sync(
    func: Callable[..., TypeVar("Result")], *args: Any, **kwargs: Any
) -> TypeVar("Result"):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, functools.partial(func, *args, **kwargs))


async def get_reply_to(
    client: pyrogram.Client,
    chat_id: int | str | None = None,
    reply_to_message_id: int | None = None,
    reply_to_story_id: int | None = None,
    message_thread_id: int | None = None,
    reply_to_chat_id: int | str | None = None,
    quote_text: str | None = None,
    quote_entities: list[types.MessageEntity] | None = None,
    parse_mode: enums.ParseMode = None,
):
    reply_to = None
    reply_to_chat = None
    if reply_to_message_id or message_thread_id:
        text, entities = (
            await parse_text_entities(client, quote_text, parse_mode, quote_entities)
        ).values()
        if reply_to_chat_id is not None:
            reply_to_chat = await client.resolve_peer(reply_to_chat_id)
        reply_to = types.InputReplyToMessage(
            reply_to_message_id=reply_to_message_id,
            message_thread_id=message_thread_id,
            reply_to_chat=reply_to_chat,
            quote_text=text,
            quote_entities=entities,
        )
    if reply_to_story_id:
        peer = await client.resolve_peer(chat_id)
        reply_to = types.InputReplyToStory(peer=peer, story_id=reply_to_story_id)
    return reply_to
