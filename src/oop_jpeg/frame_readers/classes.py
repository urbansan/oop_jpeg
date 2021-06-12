from ..byte_stream import ByteStream
from .markers import Marker
from .abstract import AbstractReader


class DqtReader(AbstractReader):
    marker = Marker.DQT


class DhtReader(AbstractReader):
    marker = Marker.DHT


class App0Reader(AbstractReader):
    marker = Marker.APP0


class UnknownReader(AbstractReader):
    marker = Marker.UNKNOWN

    def __repr__(self):
        return f"<{type(self).__name__} object with marker {self.marker!s}>"

    def consume_stream(self, stream: ByteStream):
        objects = super().consume_stream(stream)
        for obj in objects:
            obj.reader = self.marker
        return objects


class SoiReader(AbstractReader):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]


class EoiReader(AbstractReader):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]
