import pyrogram
from pyrogram import raw


class AcceptTermsOfService:
    async def accept_terms_of_service(
        self: "pyrogram.Client", terms_of_service_id: str
    ) -> bool:
        r = await self.invoke(
            raw.functions.help.AcceptTermsOfService(
                id=raw.types.DataJSON(data=terms_of_service_id)
            )
        )

        return bool(r)
