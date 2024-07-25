from io import BytesIO
from typing import cast, Union, Any

from .bool import BoolFalse, BoolTrue, Bool
from .int import Int, Long
from ..list import List
from ..tl_object import TLObject


class Vector(bytes, TLObject):
    ID = 0x1CB5C415

    # Method added to handle the special case when a query returns a bare Vector (of Ints);
    # i.e., RpcResult body starts with 0x1cb5c415 (Vector Id) - e.g., messages.GetMessagesViews.
    @staticmethod
    def read_bare(b: BytesIO, size: int) -> Union[int, Any]:
        if size == 4:
            # cek
            e = int.from_bytes(b.read(4), "little")
            # bak
            b.seek(-4, 1)
            # cond
            if e in [
                BoolFalse.ID,
                BoolTrue.ID,
            ]:
                return Bool.read(b)
            # not
            else:
                return Int.read(b)

        if size == 8:
            return Long.read(b)

        return TLObject.read(b)

    @classmethod
    def read(cls, data: BytesIO, t: Any = None, *args: Any) -> List:
        count = Int.read(data)
        left = len(data.read())
        size = (left / count) if count else 0
        data.seek(-left, 1)

        return List(
            t.read(data) if t else Vector.read_bare(data, size) for _ in range(count)
        )

    def __new__(cls, value: list, t: Any = None) -> bytes:  # type: ignore
        return b"".join(
            [Int(cls.ID, False), Int(len(value))]
            + [cast(bytes, t(i)) if t else i.write() for i in value]
        )
