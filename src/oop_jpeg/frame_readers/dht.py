from oop_jpeg.frame_readers.abstract import AbstractReader
from oop_jpeg.frame_readers.markers import Marker


class DhtReader(AbstractReader):
    marker = Marker.DHT

class DHT:
    def __init__(self, table_id, bytes_):
        pass