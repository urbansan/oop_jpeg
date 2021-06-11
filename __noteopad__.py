from oop_jpeg import ByteStream
from oop_jpeg.frames import factory_dict

from pathlib import Path
bale_jpg = Path(__file__).parent / "tests" / "data" / 'bale.jpg'

bs = ByteStream(bale_jpg)

frames = []
while bs:
    last_byte = bs.next_byte()
    if last_byte == 0xff:
        current_byte = bs.next_byte()
        try:
            marker = factory_dict[current_byte]
        except KeyError as err:
            raise RuntimeError(f'Unknown marker {hex(current_byte)}') from err
        frames += marker.consume_stream(bs)
    else:
        raise RuntimeError(f'Got different byte then 0xFF: {hex(last_byte)}')