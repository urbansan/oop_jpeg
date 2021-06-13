from ..byte_stream import ByteStream
from .markers import Marker
from .abstract import AbstractReader
from typing import List

class DQT:
    zig_zag_indexes = [
        0, 1, 8, 16, 9, 2, 3, 10,
        17, 24, 32, 25, 18, 11, 4, 5,
        12, 19, 26, 33, 40, 48, 41, 34,
        27, 20, 13, 6, 7, 14, 21, 28,
        35, 42, 49, 56, 57, 50, 43, 36,
        29, 22, 15, 23, 30, 37, 44, 51,
        58, 59, 52, 45, 38, 31, 39, 46,
        53, 60, 61, 54, 57, 55, 62, 63,
    ]

    def __init__(self, table_id, data):
        self.data = self._read_data(data)
        self.id = table_id

    def _read_data(self, data):
        return [data[i]for i in self.zig_zag_indexes]

class UnknownFrame:
    def __init__(self, data):
        self.data = data
        self.marker_used = Marker.UNKNOWN

    def __repr__(self):
        return f"<{type(self).__name__} object with marker {self.marker_used!s}>"

class DqtReader(AbstractReader):
    marker = Marker.DQT

    def _parse_bytes(self, bytes: List[int]):
        DQTs = []
        position = 0
        while len(bytes) >= position + 1:
            table_id = bytes[position] & 0xF
            if bytes[position] >> 4 == 1:
                data = self._8bit_to_16bit_step(bytes[position +1: position + 129])
                position += 129
            else:
                data = bytes[position + 1: position + 65]
                position += 65
            DQTs.append(DQT(table_id, data))
        return DQTs

    def _8bit_to_16bit_step(self, bytes):
        new_step_bytes = map(
            lambda x: (x[1] << 8) + x[0],
            zip(
                [i for i in bytes if i % 2 == 1],
                [i for i in bytes if i % 2 == 0],
            ),
        )
        return list(new_step_bytes)


class DhtReader(AbstractReader):
    marker = Marker.DHT


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


class EoiReader(AbstractReader):
    marker = Marker.SOI

    def consume_stream(self, stream: ByteStream):
        cls = type(self)
        return [cls([])]
