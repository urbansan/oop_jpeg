from typing import List

from .abstract import AbstractReader
from .markers import Marker


class DqtReader(AbstractReader):
    marker = Marker.DQT

    def _parse_bytes(self, bytes_: List[int]):
        DQTs = []
        position = 0
        while len(bytes_) >= position + 1:
            table_id = bytes_[position] & 0xF
            if bytes_[position] >> 4 == 1:
                data = self._8bit_to_16bit_step(bytes_[position + 1 : position + 129])
                position += 129
            else:
                data = bytes_[position + 1 : position + 65]
                position += 65
            dqt = DQT.from_byte_stream(table_id, data)
            DQTs.append(dqt)
        return DQTs

    @staticmethod
    def _8bit_to_16bit_step(bytes_):
        new_step_bytes = map(
            lambda x: (x[1] << 8) + x[0],
            zip(
                [i for i in bytes_ if i % 2 == 1],
                [i for i in bytes_ if i % 2 == 0],
            ),
        )
        return list(new_step_bytes)


class DQT(list):
    zig_zag_indexes = [
        (0, 0),
        (0, 1),
        (1, 0),
        (2, 0),
        (1, 1),
        (0, 2),
        (0, 3),
        (1, 2),
        (2, 1),
        (3, 0),
        (4, 0),
        (3, 1),
        (2, 2),
        (1, 3),
        (0, 4),
        (0, 5),
        (1, 4),
        (2, 3),
        (3, 2),
        (4, 1),
        (5, 0),
        (6, 0),
        (5, 1),
        (4, 2),
        (3, 3),
        (2, 4),
        (1, 5),
        (0, 6),
        (0, 7),
        (1, 6),
        (2, 5),
        (3, 4),
        (4, 3),
        (5, 2),
        (6, 1),
        (7, 0),
        (7, 1),
        (6, 2),
        (5, 3),
        (4, 4),
        (3, 5),
        (2, 6),
        (1, 7),
        (2, 7),
        (3, 6),
        (4, 5),
        (5, 4),
        (6, 3),
        (7, 2),
        (7, 3),
        (6, 4),
        (5, 5),
        (4, 6),
        (3, 7),
        (4, 7),
        (5, 6),
        (6, 5),
        (7, 4),
        (7, 5),
        (6, 6),
        (7, 1),
        (6, 7),
        (7, 6),
        (7, 7),
    ]

    def __init__(self, table_id):
        super().__init__([[0 for _ in range(8)] for _ in range(8)])
        self.id = table_id

    @classmethod
    def from_byte_stream(cls, table_id, bytes_):
        dqt = cls(table_id=table_id)
        for idx, byte in enumerate(bytes_):
            x, y = cls.zig_zag_indexes[idx]
            dqt[x][y] = byte
        return dqt

    def __repr__(self):
        return f"{type(self).__name__}(table_id={self.id})"

    # stream_zigzag = [
    #     0, 1, 8, 16, 9, 2, 3, 10,
    #     17, 24, 32, 25, 18, 11, 4, 5,
    #     12, 19, 26, 33, 40, 48, 41, 34,
    #     27, 20, 13, 6, 7, 14, 21, 28,
    #     35, 42, 49, 56, 57, 50, 43, 36,
    #     29, 22, 15, 23, 30, 37, 44, 51,
    #     58, 59, 52, 45, 38, 31, 39, 46,
    #     53, 60, 61, 54, 57, 55, 62, 63,
    # ]
