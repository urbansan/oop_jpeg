from oop_jpeg import ByteStream
from .markers import Marker
from .abstract import AbstractFrame


class DQT(AbstractFrame):
    marker = Marker.DQT


class DHT(AbstractFrame):
    marker = Marker.DHT


class APP0(AbstractFrame):
    marker = Marker.APP0


class DefaultFrame(AbstractFrame):
    marker = Marker.UNKNOWN

    def __repr__(self):
        return f"{type(self).__name__} object with marker {self.marker!s}"

    def consume_stream(self, stream: ByteStream):
        objects = super().consume_stream(stream)
        for obj in objects:
            obj.marker = self.marker
        return objects


class SOI(AbstractFrame):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]


class EOI(AbstractFrame):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]
