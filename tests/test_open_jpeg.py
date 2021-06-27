from pathlib import Path
from oop_jpeg import Jpeg
from oop_jpeg.streams import ByteStream


def test_open_jpeg(bale_jpg: Path):
    assert bale_jpg.exists()


def test_go_through_bytes(bale_jpg: Path):
    sb = ByteStream(bale_jpg)
    SOF = sb.next_byte()
    assert 0xFF == SOF


def test_reads_jpeg_bytes(bale_jpg: Path):
    Jpeg(bale_jpg)
