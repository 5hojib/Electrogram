from io import BytesIO
from json import dumps
from typing import Any, cast

from pyrogram.raw.all import objects


class TLObject:
    __slots__: list[str] = []

    QUALNAME = "Base"

    @classmethod
    def read(cls, b: BytesIO, *args: Any) -> Any:
        return cast(
            TLObject, objects[int.from_bytes(b.read(4), "little")]
        ).read(b, *args)

    def write(self, *args: Any) -> bytes:
        pass

    @staticmethod
    def default(obj: "TLObject") -> str | dict[str, str]:
        if isinstance(obj, bytes):
            return repr(obj)

        return {
            "_": obj.QUALNAME,
            **{
                attr: getattr(obj, attr)
                for attr in obj.__slots__
                if getattr(obj, attr) is not None
            },
        }

    def __str__(self) -> str:
        return dumps(
            self,
            indent=4,
            default=TLObject.default,
            ensure_ascii=False,
        )

    def __repr__(self) -> str:
        return (
            f'pyrogram.raw.{self.QUALNAME}({", ".join(f"{attr}={getattr(self, attr)!r}" for attr in self.__slots__ if getattr(self, attr) is not None)})'
            if hasattr(self, "QUALNAME")
            else repr(self)
        )

    def __eq__(self, other: Any) -> bool:
        for attr in self.__slots__:
            try:
                if getattr(self, attr) != getattr(other, attr):
                    return False
            except AttributeError:
                return False

        return True

    def __len__(self) -> int:
        return len(self.write())

    def __call__(self, *args: Any, **kwargs: Any) -> Any:
        pass

    def __hash__(self) -> int:
        return hash(
            (
                self.__class__,
                *tuple(
                    getattr(self, attr)
                    for attr in self.__slots__
                    if getattr(self, attr) is not None
                ),
            )
        )
