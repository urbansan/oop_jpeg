from enum import Enum
from pathlib import Path

from .streams import ByteStream
from .frame_readers import ReaderFactory


class Jpeg:
    def __init__(self, filename: Path):
        self.frames = self._read_frames(filename)
        print()
        # for frame in self.frames:
        #     frame.update_image_info(self)

    @staticmethod
    def _read_frames(filename: Path):
        bs = ByteStream(filename)

        frames = []
        while bs:
            last_byte = bs.next_byte()
            if last_byte == 0xFF:
                current_byte = bs.next_byte()
                if current_byte == 0xFF:
                    bs.position -= 1
                    continue
                reader = ReaderFactory(current_byte)
                new_frames = reader.consume_stream(bs)
                frames += new_frames
            else:
                raise RuntimeError(f"Got different byte then 0xFF: {hex(last_byte)}")
        return frames
