import pyrogram
from pyrogram import raw


class GetDialogsCount:
    async def get_dialogs_count(
        self: "pyrogram.Client", pinned_only: bool = False
    ) -> int:
        if pinned_only:
            return len(
                (
                    await self.invoke(
                        raw.functions.messages.GetPinnedDialogs(folder_id=0)
                    )
                ).dialogs
            )
        else:
            r = await self.invoke(
                raw.functions.messages.GetDialogs(
                    offset_date=0,
                    offset_id=0,
                    offset_peer=raw.types.InputPeerEmpty(),
                    limit=1,
                    hash=0,
                )
            )

            if isinstance(r, raw.types.messages.Dialogs):
                return len(r.dialogs)
            else:
                return r.count
