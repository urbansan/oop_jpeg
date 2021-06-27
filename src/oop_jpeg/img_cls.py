from enum import Enum
from pathlib import Path

from .streams import ByteStream
from .marker_readers import ReaderFactory
from .marker_readers.abstract import AbstractMarker
from typing import Iterable


class Jpeg:
    def __init__(self, filename: Path):
        markers = self._read_frames(filename)
        self.unknown_markers = []
        self.dqt = {}
        self.dht = {}
        for marker in markers:
            marker.update_jpeg_obj(self)
        self.mcus = self.decode_huffman_bitstream()
        print()

    def decode_huffman_bitstream(self):
        pass




    @staticmethod
    def _read_frames(filename: Path) -> Iterable[AbstractMarker]:
        bs = ByteStream(filename)

        markers = []
        while bs:
            last_byte = bs.next_byte()
            if last_byte == 0xFF:
                current_byte = bs.next_byte()
                if current_byte == 0xFF:
                    bs.position -= 1
                    continue
                reader = ReaderFactory(current_byte)
                new_markers = reader.consume_stream(bs)
                markers += new_markers
            else:
                raise RuntimeError(f"Got different byte then 0xFF: {hex(last_byte)}")
        return markers
