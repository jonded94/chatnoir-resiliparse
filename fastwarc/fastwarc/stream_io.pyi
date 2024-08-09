from types import TracebackType
from typing import ContextManager, IO, Optional, Type, Union, BinaryIO


class IOStream(ContextManager[IOStream]):
    def read(self, size: int) -> bytes: ...
    def write(self, data: bytes) -> int: ...
    def close(self) -> None: ...
    def flush(self) -> None: ...
    def seek(self, offset: int) -> None: ...
    def tell(self) -> int: ...
    def __enter__(self) -> IOStream: ...
    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        traceback: Optional[TracebackType]
    ) -> None: ...


class BufferedReader:
    def __init__(
        self, stream: Union[IOStream, BinaryIO], buf_size: int = 65536, negotiate_stream: bool = True
    ) -> None: ...
    def close(self) -> None: ...
    def consume(self, size: int = -1) -> int: ...
    def read(self, size: int = -1) -> bytes: ...
    def readline(self, crlf: bool = True, max_line_len: int = 8192) -> bytes: ...
    def tell(self) -> int: ...


class BytesIOStream(IOStream):
    def __init__(self, initial_data: Union[bytes, None] = None) -> None: ...
    def getvalue(self) -> bytes: ...


class FileStream(IOStream):
    def __init__(self, filename: str, mode: str = "rb") -> None: ...


class CompressingStream(IOStream):
    def begin_member(self) -> int: ...
    def end_member(self) -> int: ...


class BrotliStream(CompressingStream):
    def __init__(
        self, raw_stream: Union[IOStream, BinaryIO], quality: int = 11, lgwin: int = 22, lgblock: int = 0
    ) -> None: ...


class GZipStream(CompressingStream):
    def __init__(
        self, raw_stream: Union[IOStream, BinaryIO], compression_level: int = 9, zlib: bool = False
    ) -> None: ...


class LZ4Stream(CompressingStream):
    def __init__(
        self,
        raw_stream: Union[IOStream, BinaryIO],
        compression_level: int = 12,
        favor_dec_speed: bool = True,
    ) -> None: ...
    def prepopulate(self, initial_data: bytes) -> None: ...


class PythonIOStreamAdapter(IOStream):
    def __init__(self, py_stream: BinaryIO) -> None: ...


class FastWARCError(Exception):
    pass


class ReaderStaleError(FastWARCError):
    pass


class StreamError(FastWARCError):
    pass
