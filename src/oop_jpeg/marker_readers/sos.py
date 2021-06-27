from typing import List, Dict
from collections import namedtuple

from .abstract import AbstractReader, AbstractMarker
from .markers import Marker
from ..streams import ByteStream, BitStream


AcDc = namedtuple("AcDc", ["ac", "dc"])


class SOS(AbstractMarker):
    def update_jpeg_obj(self, jpeg_obj):
        jpeg_obj.sos = self

    def __init__(self):
        self.color_id_to_huffman_table_ids: Dict[int, AcDc] = {}
        self.start_of_selection = 0
        self.end_of_selection = 63
        self.successive_approximation = 0
        self.huffman_bytes = []

    def __repr__(self):
        return f"{type(self).__name__}()"

    def _get_hft(self, color_id):
        try:
            return self.color_id_to_huffman_table_ids[color_id]
        except KeyError as err:
            raise RuntimeError(f"No color id data in SOS object: '{color_id}'")

    def add_color_component(
        self,
        color_id,
        ac_huffman_table_id,
        dc_huffman_table_id,
    ):
        self.color_id_to_huffman_table_ids[color_id] = AcDc(
            dc_huffman_table_id, ac_huffman_table_id
        )

    def read_huffman_bitstream(self, stream: ByteStream):
        while stream:
            last_byte = stream.next_byte()
            if last_byte == 0xFF:
                current_byte = stream.next_byte()
                if current_byte == 0x00:
                    self.huffman_bytes.append(last_byte)
                elif current_byte == 0xFF:
                    stream.position -= 1  # skip previous byte
                    continue
                elif Marker.RST0.value <= current_byte <= Marker.RST7.value:
                    pass  # skip restart markers
                elif current_byte == Marker.EOI.value:
                    break  # break the loop
            else:
                self.huffman_bytes.append(last_byte)

    @classmethod
    def from_byte_stream(cls, bytes_):
        sos = cls()
        color_components_count = bytes_[0]

        idx = 0
        for idx in range(color_components_count):
            component_id = bytes_[1 + idx * 2]
            huffman_tables = bytes_[2 + idx * 2]
            dc = huffman_tables & 0xF
            ac = huffman_tables >> 4
            sos.add_color_component(component_id, ac, dc)

        last_position = 3 + idx * 2
        (
            sos.start_of_selection,
            sos.end_of_selection,
            sos.successive_approximation,
        ) = bytes_[last_position : last_position + 3]
        remaining_bytes = bytes_[last_position + 3 :]
        if remaining_bytes:
            raise RuntimeError(
                f"There are to many bytes remaining after SOS component header length: {remaining_bytes}"
            )
        return sos


class SosReader(AbstractReader):
    marker = Marker.SOS

    def consume_stream(self, stream: ByteStream):
        sos = super().consume_stream(stream)
        sos.read_huffman_bitstream(stream)
        return [sos]

    def _parse_bytes(self, bytes_: List[int]):
        return SOS.from_byte_stream(bytes_)
