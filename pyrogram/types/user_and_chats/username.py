#  Pyrofork - Telegram MTProto API Client Library for Python
#  Copyright (C) 2022-present Mayuri-Chan <https://github.com/Mayuri-Chan>
#
#  This file is part of Pyrofork.
#
#  Pyrofork is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrofork is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrofork.  If not, see <http://www.gnu.org/licenses/>.


from typing import TYPE_CHECKING

from pyrogram.types.object import Object

if TYPE_CHECKING:
    from pyrogram import raw


class Username(Object):
    """A Username.


    Parameters:
        username (``String``):
            The channel/user username.

        editable (``bool``, *optional*):
            Can the username edited.

        active (``bool``, *optional*)
            Is the username active.
    """

    def __init__(
        self,
        *,
        username: str,
        editable: bool | None = None,
        active: bool | None = None,
    ):
        super().__init__()

        self.username = username
        self.editable = editable
        self.active = active

    @staticmethod
    def _parse(action: "raw.types.Username") -> "Username":
        return Username(
            username=getattr(action, "username", None),
            editable=getattr(action, "editable", None),
            active=getattr(action, "active", None),
        )
