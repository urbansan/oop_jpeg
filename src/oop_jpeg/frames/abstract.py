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

    def consume_stream(self, stream: ByteStream):
        """:return count of consumed bytes"""
        cls = type(self)
        length = (stream.next_byte() << 8) + stream.next_byte()
        bytes = stream.next_bytes(length - 2)
        objects = [cls(data) for data in cls._parse_bytes(bytes)]
        return objects

    @staticmethod
    def _parse_bytes(bytes: Iterable[int]):
        return [bytes]
