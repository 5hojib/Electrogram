from typing import Any, NoReturn, Union

from bson.codec_options import CodecOptions
from pymongo.client_session import TransactionOptions
from pymongo.read_concern import ReadConcern
from pymongo.read_preferences import (
    Nearest,
    Primary,
    PrimaryPreferred,
    Secondary,
    SecondaryPreferred,
)
from pymongo.write_concern import WriteConcern

try:
    from typing import Protocol, runtime_checkable
except ImportError:
    from typing_extensions import Protocol, runtime_checkable

ReadPreferences = Union[
    Primary, PrimaryPreferred, Secondary, SecondaryPreferred, Nearest
]


@runtime_checkable
class DummyMongoClient(Protocol):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError

    def get_database(
        self,
        name: str | None = None,
        *,
        codec_options: CodecOptions | None = None,
        read_preference: ReadPreferences | None = None,
        write_concern: WriteConcern | None = None,
        read_concern: ReadConcern | None = None,
    ) -> NoReturn:
        raise NotImplementedError

    async def start_session(
        self,
        *,
        causal_consistency: bool | None = None,
        default_transaction_options: TransactionOptions | None = None,
        snapshot: bool = False,
    ) -> NoReturn:
        raise NotImplementedError
