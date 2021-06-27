from typing import List
from collections import namedtuple

from .abstract import AbstractReader, AbstractMarker
from .markers import Marker

SaQt = namedtuple("SaQt", ["sampling_factor", "qt_table_id"])


class SOF(AbstractMarker):
    def __init__(self, precision, height, width):
        self.precision = precision
        self.height = height
        self.width = width
        self.component_id_to_data = {}

    def update_jpeg_obj(self, jpeg_obj):
        jpeg_obj.height = self.height
        jpeg_obj.width = self.width
        jpeg_obj.precision = self.precision

    def add_component(self, component_id, sampling_factor, quantization_table_id):
        self.component_id_to_data[component_id] = SaQt(
            sampling_factor, quantization_table_id
        )


class SofReader(AbstractReader):
    marker = Marker.SOF

    def _parse_bytes(self, bytes_: List[int]):
        precision = bytes_[0]
        height = (bytes_[1] << 8) | bytes_[2]
        width = (bytes_[3] << 8) | bytes_[4]
        sof = SOF(precision, height, width)
        components_count = bytes_[5]
        for idx in range(components_count):
            component_id = bytes_[6 + idx * 3]
            sampling_factor = bytes_[7 + idx * 3]
            quantization_table_id = bytes_[8 + idx * 3]
            sof.add_component(component_id, sampling_factor, quantization_table_id)
        return [sof]
