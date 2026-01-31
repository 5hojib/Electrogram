from __future__ import annotations

import typing
from datetime import datetime
from enum import Enum
from json import dumps

if typing.TYPE_CHECKING:
    import pyrogram


class Object:
    def __init__(self, client: pyrogram.Client = None) -> None:
        self._client = client

    def bind(self, client: pyrogram.Client) -> None:
        """Bind a Client instance to this and to all nested Pyrogram objects.

        Parameters:
            client (:obj:`~pyrogram.types.Client`):
                The Client instance to bind this object with. Useful to re-enable bound methods after serializing and
                deserializing Pyrogram objects with ``repr`` and ``eval``.
        """
        self._client = client

        for i in self.__dict__:
            o = getattr(self, i)

            if isinstance(o, Object):
                o.bind(client)

    @staticmethod
    def default(obj: Object):
        if isinstance(obj, bytes):
            return repr(obj)

        if isinstance(obj, typing.Match):
            return repr(obj)

        if isinstance(obj, Enum):
            return str(obj)

        if isinstance(obj, datetime):
            return str(obj)

        attributes_to_hide = ["raw"]

        filtered_attributes = {
            attr: ("*" * 9 if attr == "phone_number" else getattr(obj, attr))
            for attr in filter(
                lambda x: not x.startswith("_") and x not in attributes_to_hide,
                obj.__dict__,
            )
            if getattr(obj, attr) is not None
        }

        return {"_": obj.__class__.__name__, **filtered_attributes}

    def __str__(self) -> str:
        return dumps(self, indent=4, default=Object.default, ensure_ascii=False)

    def __repr__(self) -> str:
        return "pyrogram.types.{}({})".format(
            self.__class__.__name__,
            ", ".join(
                f"{attr}={getattr(self, attr)!r}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
                if getattr(self, attr) is not None
            ),
        )

    def __eq__(self, other: Object) -> bool:
        for attr in self.__dict__:
            try:
                if attr.startswith("_"):
                    continue

                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __setstate__(self, state):
        for attr in state:
            obj = state[attr]

            # Maybe a better alternative would be https://docs.python.org/3/library/inspect.html#inspect.signature
            if isinstance(obj, tuple) and len(obj) == 2 and obj[0] == "dt":
                state[attr] = datetime.fromtimestamp(obj[1])

        self.__dict__ = state

    def __getstate__(self):
        state = self.__dict__.copy()
        state.pop("_client", None)

        for attr in state:
            obj = state[attr]

            if isinstance(obj, datetime):
                state[attr] = ("dt", obj.timestamp())

        return state
