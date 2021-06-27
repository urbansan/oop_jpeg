from typing import List

from .abstract import AbstractReader, AbstractMarker
from .markers import Marker


class DhtReader(AbstractReader):
    marker = Marker.DHT

    def _parse_bytes(self, bytes_: List[int]):
        # a = [hex(b) for b in bytes_]
        dhts = self._from_byte_stream(bytes_)
        return dhts

    def _from_byte_stream(self, bytes_):
        remaining_bytes = bytes_
        dhts = []
        while remaining_bytes:
            dht, remaining_bytes = DHT.from_byte_stream(bytes_)
            dhts.append(dht)
        return dhts


class DHT(AbstractMarker):
    dht_type = None

    def update_jpeg_obj(self, jpeg_obj):
        jpeg_obj.dht[self.id] = self

    def __init__(self, table_id, symbols: list):
        self.id = table_id
        self.symbols = symbols
        self.code_to_symbol = self.generate_codes(symbols)

    @staticmethod
    def generate_codes(symbols):
        code = 0
        code_to_symbol = {}
        for common_symbols in symbols:
            for symbol in common_symbols:
                code_to_symbol[code] = symbol
                code += 1
            code <<= 1

        return code_to_symbol

    def __repr__(self):
        return f"{type(self).__name__}(table_id={self.id})"

    @classmethod
    def from_byte_stream(cls, bytes_):
        table_type = bytes_[0] >> 4
        table_id = bytes_[0] & 0xF
        symbol_count = bytes_[1:17]
        sum_of_symbols = sum(symbol_count)
        symbols = bytes_[17 : 17 + sum_of_symbols + 1]
        temp_list = []
        total_length = 0
        for idx, length in enumerate(symbol_count):
            temp_list.append(symbols[total_length : total_length + length])
            total_length += length
        dht = cls.from_table_type(table_type, table_id, temp_list)

        remaining_bytes = bytes_[17 + sum_of_symbols + 1 :]
        return dht, remaining_bytes

    @classmethod
    def from_table_type(cls, table_type, table_id, symbols):
        for subcls in cls.__subclasses__():
            if subcls.dht_type == table_type:
                return subcls(table_id, symbols)


class DHTac(DHT):
    dht_type = 1


class DHTdc(DHT):
    dht_type = 0
