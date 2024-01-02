import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class StoryForwardHeader(Object):
    def __init__(
        self, *,
        user: "types.User" = None,
        sender_name: str = None,
        chat: "types.Chat" = None,
        story_id: int = None,
        is_modified: bool = None
    ):
        super().__init__()

        self.user = user
        self.sender_name = sender_name
        self.chat = chat
        self.story_id = story_id
        self.is_modified = is_modified

    async def _parse(
        client: "pyrogram.Client",
        fwd_header: "raw.types.StoryFwdHeader"
    ) -> "StoryForwardHeader":
        user = None
        chat = None
        if fwd_header.from_peer is not None:
            if isinstance(fwd_header.from_peer, raw.types.PeerChannel):
                chat = await client.get_chat(utils.get_channel_id(fwd_header.from_peer.channel_id))
            elif isinstance(fwd_header.from_peer, raw.types.InputPeerSelf):
                user = client.me
            else:
                user = await client.get_users(fwd_header.from_peer.user_id)
        
        return StoryForwardHeader(
            user=user,
            sender_name=fwd_header.from_name,
            chat=chat,
            story_id=fwd_header.story_id,
            is_modified=fwd_header.modified
        )
