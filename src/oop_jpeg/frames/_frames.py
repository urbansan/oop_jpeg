from oop_jpeg import ByteStream
from .markers import Marker
from .abstract import AbstractFrame


class DQT(AbstractFrame):
    marker = Marker.DQT.value


class DHT(AbstractFrame):
    marker = Marker.DHT.value


class DefaultFrame(AbstractFrame):
    marker = None


class SOI(AbstractFrame):
    marker = Marker.SOI.value

    @classmethod
    def consume_stream(cls, stream: ByteStream):
        return [cls([])]
