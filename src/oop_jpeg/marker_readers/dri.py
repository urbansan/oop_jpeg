from typing import List

from .abstract import AbstractReader, AbstractMarker
from .markers import Marker


class DRI(AbstractMarker):
    def update_jpeg_obj(self, jpeg_obj):
        jpeg_obj.dri_interval = self.interval

    def __init__(self, interval: int):
        self.interval = interval


class DriReader(AbstractReader):
    marker = Marker.DRI

    def _parse_bytes(self, bytes_: List[int]):
        interval = (bytes_[1] << 8) + bytes_[0]
        return DRI(interval)
