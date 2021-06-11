from oop_jpeg import ByteStream

from .abstract import AbstractFrame


class SofFrame(AbstractFrame):
    marker = 0xFF

    def consume_stream(self, stream: ByteStream):
        pass
