import abc
from typing import List
from ..streams import ByteStream


class AbstractReader(abc.ABC):
    @property
    @abc.abstractmethod
    def marker(self) -> int:
        ...

    def __init__(self, data):
        self.data = data

    def consume_stream(self, stream: ByteStream):
        """:return count of consumed bytes"""
        length = (stream.next_byte() << 8) + stream.next_byte()
        bytes = stream.next_bytes(length - 2)
        return self._parse_bytes(bytes)

    def _parse_bytes(self, bytes: List[int]):
        return [bytes]
