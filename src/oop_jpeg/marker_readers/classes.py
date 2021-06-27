from ..streams import ByteStream
from .markers import Marker
from .abstract import AbstractReader, AbstractMarker, UnknownMarker
from typing import List, Iterable


# class UnknownMarker:
#     def __init__(self, data):
#         self.data = data
#         self.marker_used = Marker.UNKNOWN
#
#     def __repr__(self):
#         return f"<{type(self).__name__} object with marker {self.marker_used!s}>"


class App0Reader(AbstractReader):
    marker = Marker.APP0


class UnknownReader(AbstractReader):
    marker = Marker.UNKNOWN

    def consume_stream(self, stream: ByteStream):
        objects = super().consume_stream(stream)
        for obj in objects:
            obj.marker_used = self.marker
        return objects


class SoiReader(AbstractReader):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        marker_obj = UnknownMarker([])
        marker_obj.marker_used = self.marker
        return [marker_obj]


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
