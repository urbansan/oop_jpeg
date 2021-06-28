from oop_jpeg.streams import BitStream
from oop_jpeg.img_cls import Jpeg
from oop_jpeg.marker_readers.sos import SOS


def test_bit_streamer_correctness(bale_jpg):
    markers = Jpeg._read_frames(bale_jpg)

    for marker in markers:
        if isinstance(marker, SOS):
            break

    assert 0 < len(marker.huffman_bytes)
    bit_stream = BitStream(marker.huffman_bytes)

    translated_bytes = [bit_stream.next_bits(8) for _ in marker.huffman_bytes]
    assert len(marker.huffman_bytes) == len(translated_bytes)
    assert marker.huffman_bytes == translated_bytes


def test_bit_streamer_correctness_bit_by_bit(bale_jpg):
    markers = Jpeg._read_frames(bale_jpg)

    for marker in markers:
        if isinstance(marker, SOS):
            break
    assert 0 < len(marker.huffman_bytes)
    bit_stream = BitStream(marker.huffman_bytes)

    translated_bytes = [
        bit_stream._merge_bits([bit_stream.next_bit() for _ in range(8)])
        for _ in marker.huffman_bytes
    ]
    assert len(marker.huffman_bytes) == len(translated_bytes)
    assert marker.huffman_bytes == translated_bytes


def test_bit_streamer_correctness_mixed_bits(bale_jpg):
    markers = Jpeg._read_frames(bale_jpg)

    for marker in markers:
        if isinstance(marker, SOS):
            break
    assert 0 < len(marker.huffman_bytes)
    bit_stream = BitStream(marker.huffman_bytes)

    translated_bytes = [
        bit_stream._merge_bits([bit_stream.next_bits(7), bit_stream.next_bit()])
        for _ in marker.huffman_bytes
    ]
    assert len(marker.huffman_bytes) == len(translated_bytes)
    assert marker.huffman_bytes == translated_bytes
