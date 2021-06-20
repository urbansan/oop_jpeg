from ..byte_stream import ByteStream
from .markers import Marker
from .abstract import AbstractReader
from typing import List, Iterable


class UnknownFrame:
    def __init__(self, data):
        self.data = data
        self.marker_used = Marker.UNKNOWN

    def __repr__(self):
        return f"<{type(self).__name__} object with marker {self.marker_used!s}>"


class App0Reader(AbstractReader):
    marker = Marker.APP0


class UnknownReader(AbstractReader):
    marker = Marker.UNKNOWN

    def consume_stream(self, stream: ByteStream):
        objects = super().consume_stream(stream)
        for obj in objects:
            obj.marker_used = self.marker
        return objects

    def _parse_bytes(self, bytes: List[int]):
        return [UnknownFrame(bytes)]


class SoiReader(AbstractReader):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]


# class EoiReader(AbstractReader):
#     marker = Marker.SOI
#
#     def consume_stream(self, stream: ByteStream):
#         cls = type(self)
#         return [cls([])]


class COM:
    def __init__(self, bytes_: Iterable[int]):
        self._bytes = bytes_

    def get_text(self):
        raise NotImplemented


class ComReader(AbstractReader):
    marker = Marker.COM

    def _parse_bytes(self, bytes_: List[int]):
        return [COM(bytes_)]
