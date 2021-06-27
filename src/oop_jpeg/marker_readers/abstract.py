import abc
from typing import List
from ..streams import ByteStream
from .markers import Marker


class AbstractMarker(abc.ABC):
    @abc.abstractmethod
    def update_jpeg_obj(self, jpeg_obj):
        ...


class UnknownMarker(AbstractMarker):
    def update_jpeg_obj(self, jpeg_obj):
        jpeg_obj.unknown_markers.append(self)


    def __init__(self, data):
        self.data = data
        self.marker_used = Marker.UNKNOWN

    def __repr__(self):
        return f"<{type(self).__name__} object with marker {self.marker_used!s}>"


class AbstractReader(abc.ABC):
    @property
    @abc.abstractmethod
    def marker(self) -> int:
        ...

    def __init__(self, data):
        self.data = data

    def consume_stream(self, stream: ByteStream) -> List[AbstractMarker]:
        """:return count of consumed bytes"""
        length = (stream.next_byte() << 8) + stream.next_byte()
        bytes_ = stream.next_bytes(length - 2)
        return self._parse_bytes(bytes_)

    def _parse_bytes(self, bytes_: List[int]):
        return [UnknownMarker(bytes_)]
