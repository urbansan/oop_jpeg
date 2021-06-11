import abc
from typing import Iterable
from ..byte_stream import ByteStream


class AbstractFrame(abc.ABC):
    @property
    @abc.abstractmethod
    def marker(self) -> int:
        ...

    def __init__(self, data):
        self.data = data

    @classmethod
    def consume_stream(cls, stream: ByteStream):
        """:return count of consumed bytes"""
        length = stream.next_byte() << 8 & stream.next_byte()
        bytes = stream.next_bytes(length - 2)
        objects = [cls(data) for data in cls._parse_bytes(bytes)]
        return objects

    @classmethod
    def _parse_bytes(self, bytes: Iterable[int]):
        return []
