from typing import List

from .abstract import AbstractReader
from .markers import Marker


class DhtReader(AbstractReader):
    marker = Marker.DHT

    def _parse_bytes(self, bytes_: List[int]):
        # a = [hex(b) for b in bytes_]
        dhts = DHT.from_byte_stream(bytes_)
        return dhts


class DHT(list):
    def __init__(self, table_id, ac_dc_table_type):
        super().__init__()
        self.id = table_id
        self._ac_dc = ac_dc_table_type

    def __repr__(self):
        return f"DHT-AC(table_id={self.id})" if self._ac_dc else f"DHT-DC(table_id={self.id})"

    @classmethod
    def from_byte_stream(cls, bytes_):
        remaining_bytes = bytes_
        dhts = []
        while remaining_bytes:
            dht, remaining_bytes = cls.parse_dht(bytes_)
            dhts.append(dht)
        print()
        return dhts
        # hex_symbols = [(hex(s >> 0xF), hex(s & 0xF)) for s in symbols]

    @classmethod
    def parse_dht(cls, bytes_):
        table_type = bytes_[0] >> 4
        table_id = bytes_[0] & 0xF
        symbol_count = bytes_[1:17]
        sum_of_symbols = sum(symbol_count)
        symbols = bytes_[17 : 17 + sum_of_symbols + 1]
        dht = cls(table_id, table_type)
        total_length = 0
        for idx, length in enumerate(symbol_count):
            dht.append(symbols[total_length : total_length + length])
            total_length += length

        remaining_bytes = bytes_[17 + sum_of_symbols + 1:]
        return dht, remaining_bytes

    @property
    def dc(self):
        return self._ac_dc == 0

    @property
    def ac(self):
        return self._ac_dc == 1
