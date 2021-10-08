import typing as t

_SIZE: t.Final[int] = 4
_META: t.Final[bytes] = b','


class Chunk(t.NamedTuple):
    size: int
    data: bytes


class ReadStream:
    def __init__(
        self,
        file: t.BinaryIO,
    ) -> None:
        assert not file.closed

        self.file = file
        self._meta: t.Optional[tuple[bytes, ...]] = None
        self._seek: t.Optional[int] = None

    def reset(self, fake: bool = True) -> None:
        if not fake:
            self._meta = None
            self._seek = None

            self.file.seek(0)
            return

        if self._seek:
            self.file.seek(self._seek)

    def __iter__(
        self
    ) -> t.Generator[Chunk, t.Any, t.Any]:
        read = self.file.read

        if self._meta is None:
            self.file.seek(0)

            length = read(_SIZE)
            length = int(length)

            self._seek = length + _SIZE

            bytes_ = read(length)

            metadata = bytes_.split(_META)
            self._meta = tuple(metadata)

        while (raw_size := read(_SIZE)) != b'':
            size = int(raw_size)
            data = read(size)

            yield Chunk(size, data)
