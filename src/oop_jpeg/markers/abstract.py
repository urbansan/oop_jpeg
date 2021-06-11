import abc
from ..byte_stream import ByteStream


class AbstractFrame(abc.ABC):
    @property
    @abc.abstractmethod
    def byte_marker(self):
        ...

    def is_marker_start(self, marker: int):
        return self.byte_marker == marker

    @abc.abstractmethod
    def consume_stream(self, stream: ByteStream):
        ...
