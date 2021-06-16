from typing import List

from .abstract import AbstractReader
from .markers import Marker


class DRI:
    def __init__(self, interval: int):
        self.interval = interval


class DriReader(AbstractReader):
    marker = Marker.DRI

    def _parse_bytes(self, bytes_: List[int]):
        interval = (bytes_[1] << 8) + bytes_[0]
        return DRI(interval)
