from datetime import datetime
from typing import (
    Union,
    Optional,
    Iterator,
    Dict,
    Tuple,
    Literal,
    Callable,
    Iterable,
    ValuesView,
    KeysView,
    BinaryIO,
    Protocol,
)
from enum import IntFlag

from .stream_io import BufferedReader, IOStream

class _ReadableStream(Protocol):
    def read(self, size: int) -> bytes: ...
    def seek(self, offset: int) -> int: ...

class _WritableStream(Protocol):
    def write(self, data: bytes) -> int: ...
    def flush(self) -> None: ...


class WarcRecordType(IntFlag):
    warcinfo = 2
    response = 4
    resource = 8
    request = 16
    metadata = 32
    revisit = 64
    conversion = 128
    continuation = 256
    unknown = 512
    any_type = 65535
    no_type = 0


no_type = WarcRecordType.no_type
any_type = WarcRecordType.any_type


class WarcHeaderMap:
    reason_phrase: Optional[str]
    status_code: Optional[str]
    status_line: str

    def append(self, key: str, value: str) -> None: ...
    def asdict(self) -> Dict[str, str]: ...
    def astuples(self) -> Tuple[Tuple[str, str], ...]: ...
    def clear(self) -> None: ...
    def get(self, key: str, default: Optional[str] = None) -> Optional[str]: ...
    def items(self) -> Iterator[Tuple[str, str]]: ...
    def keys(self) -> KeysView[str]: ...
    def values(self) -> ValuesView[str]: ...
    def write(self, stream: IOStream) -> None: ...
    def __getitem__(self, item: str) -> str: ...
    def __iter__(self) -> Iterator[Tuple[str, str]]: ...
    def __len__(self) -> int: ...
    def __setitem__(self, key: str, value: str) -> None: ...
    def __contains__(self, item: str) -> bool: ...


class WarcRecord:
    record_id: str
    record_type: WarcRecordType
    content_length: int
    record_date: Optional[datetime]
    headers: WarcHeaderMap
    is_http: bool
    is_http_parsed: bool
    http_headers: Optional[WarcHeaderMap]
    http_content_type: Optional[str]
    http_charset: Optional[str]
    http_date: Optional[datetime]
    http_last_modified: Optional[datetime]
    reader: BufferedReader
    stream_pos: int

    def init_headers(
        self, content_length: int = 0, record_type: WarcRecordType = no_type, record_urn: Optional[bytes] = None
    ) -> None: ...
    def freeze(self) -> bool: ...
    def set_bytes_content(self, content: bytes) -> None: ...
    def parse_http(self, strict_mode: bool = True, auto_decode: str = "none") -> None: ...
    def verify_block_digest(self, consume: bool = False) -> bool: ...
    def verify_payload_digest(self, consume: bool = False) -> bool: ...
    def write(
        self,
        stream: Union[IOStream, BinaryIO, _WritableStream],
        checksum_data: bool = False,
        payload_digest: Optional[bytes] = None,
        chunk_size: int = 16384
    ) -> int: ...



class ArchiveIterator(Iterable[WarcRecord]):
    def __init__(
        self,
        stream: Union[IOStream, BinaryIO, _ReadableStream],
        record_types: WarcRecordType = any_type,
        parse_http: bool = True,
        min_content_length: int = -1,
        max_content_length: int = -1,
        func_filter: Optional[Callable[[WarcRecord], bool]] = None,
        verify_digests: bool = False,
        strict_mode: bool = True,
        auto_decode: Literal["none", "content", "transfer", "all"] = "none",
    ) -> None: ...
    def __iter__(self) -> Iterator[WarcRecord]: ...
    def __next__(self) -> WarcRecord: ...
