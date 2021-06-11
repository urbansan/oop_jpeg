from pathlib import Path
from oop_jpeg import ByteStream


def test_open_jpeg(bale_jpg: Path):
    assert bale_jpg.exists()


def test_go_through_bytes(bale_jpg: Path):
    sb = ByteStream(bale_jpg)
    SOF = sb.next_byte()
    assert 0xFF == SOF
