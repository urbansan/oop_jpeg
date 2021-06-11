from oop_jpeg import ByteStream
from oop_jpeg.frames import MarkerFactory

from pathlib import Path
bale_jpg = Path(__file__).parent / "tests" / "data" / 'bale.jpg'

bs = ByteStream(bale_jpg)

frames = []
while bs:
    last_byte = bs.next_byte()
    if last_byte == 0xff:
        current_byte = bs.next_byte()
        if current_byte == 0xff:
            bs.position -= 1
            continue
        marker = MarkerFactory(current_byte)

        new_frames = marker.consume_stream(bs)
        frames += new_frames
    else:
        raise RuntimeError(f'Got different byte then 0xFF: {hex(last_byte)}')