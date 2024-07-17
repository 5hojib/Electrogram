import pyrogram


class ExportSessionString:
    async def export_session_string(self: "pyrogram.Client"):
        return await self.storage.export_session_string()
