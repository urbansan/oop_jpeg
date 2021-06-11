from oop_jpeg import ByteStream

from pathlib import Path
comics_jpg = Path(__file__).parent / "tests" / "data" / 'bale.jpg'

bs = ByteStream(comics_jpg)

print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())
print(bs.next_byte())