from enum import Enum
from pathlib import Path

from .streams import ByteStream, BitStream
from .marker_readers import ReaderFactory
from .marker_readers.util import ZIGZAG
from .marker_readers.abstract import AbstractMarker
from .marker_readers.sos import SOS
from typing import Iterable, List, Optional


class HuffmanBitStreamDecoder:
    def __init__(self, sos_marker: SOS, restart_interval=-1):
        self.sos = sos_marker
        self.prev_dcs = {
            color_id: 0
            for color_id in sos_marker.color_id_to_huffman_table_ids
        }
        self.restart_interval = restart_interval

    def decode_huffman_bitstream(self, mcus_count: int, dht_acs: dict, dht_dcs: dict):
        bit_stream = BitStream(self.sos.huffman_bytes)
        mcus = []
        while not bit_stream.is_finished and len(mcus) <= mcus_count:
            mcu = {}
            for color_id, (
                ac_id,
                dc_id,
            ) in self.sos.color_id_to_huffman_table_ids.items():
                dc_table = dht_dcs[dc_id]
                ac_table = dht_acs[ac_id]
                component = [[0] * 8 for _ in range(8)]

                component[0][0] = self.get_dc_coefficient(bit_stream, dc_table, color_id, len(mcus))
                try:
                    self.update_component_with_ac_coefficients(
                        component, bit_stream, ac_table
                    )
                except:
                    print(len(mcus))
                mcu[color_id] = component
            mcus.append(mcu)
        return mcus

    def reset_dc_intervals(self, color_id, mcus_size: int):
        if mcus_size % self.restart_interval == 0 and self.restart_interval > 0:
            self.prev_dcs[color_id] = 0

    def update_component_with_ac_coefficients(
        self, component: List[List[int]], bit_stream, ac_table
    ):
        idx = 1
        while idx < 64:
            symbol = self.get_next_symbol(ac_table, bit_stream)
            if symbol == 0x00:
                break
            elif symbol == 0xF0:
                idx += 16
            else:
                number_of_zeros, length = symbol >> 4, symbol & 0xF
                idx += number_of_zeros
                coeff = bit_stream.next_bits(length)
                x, y = ZIGZAG[idx]
                component[x][y] = self.decode_coefficient(coeff, length)
                idx += 1

    def get_dc_coefficient(self, bit_stream, dc_table, color_id, mcus_size: int):
        self.reset_dc_intervals(color_id, mcus_size)
        length = self.get_next_symbol(dc_table, bit_stream)
        coefficient = bit_stream.next_bits(length) if length > 0 else 0
        coefficient = self.decode_coefficient(coefficient, length)
        coefficient += self.prev_dcs[color_id]
        self.prev_dcs[color_id] = coefficient
        return coefficient

    @staticmethod
    def get_next_symbol(dht_table, stream: BitStream):
        bits = 0
        for _ in range(16):
            bits = stream.next_bit(bits)
            if bits in dht_table.code_to_symbol:
                symbol = dht_table.code_to_symbol[bits]
                return symbol
        else:
            raise ValueError(
                f"Value {bin(bits)} (or {bits!s}) not found in DHT table {repr(dht_table)}"
            )

    @staticmethod
    def decode_coefficient(coefficient: int, length: int):
        if length != 0 and coefficient < (1 << (length - 1)):
            coefficient -= (1 << length) - 1
        return coefficient


class Jpeg:
    def __init__(self, filename: Path):
        markers = self._read_frames(filename)
        self.unknown_markers = []
        self.sos: Optional[SOS, None] = None
        self.dqt = {}
        self.dht_ac = {}
        self.dht_dc = {}
        self.height = 0
        self.width = 0
        self.precision = 0
        for marker in markers:
            marker.update_jpeg_obj(self)

        mcu_count = ((self.height + self.precision - 1) // self.precision) * (
            (self.width + self.precision - 1) // self.precision
        )
        self.mcus = HuffmanBitStreamDecoder(self.sos).decode_huffman_bitstream(
            mcu_count, self.dht_ac, self.dht_dc
        )
        print()

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
