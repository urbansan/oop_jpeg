from ..utils import get_subclasses
from .abstract import AbstractReader
from .markers import Marker
from .classes import UnknownReader


factory_dict = {}
for cls in get_subclasses(AbstractReader):
    factory_dict[cls.marker.value] = cls


def ReaderFactory(byte):
    cls = factory_dict.get(byte)
    if cls is None:
        default_frame = UnknownReader([])
        try:
            default_frame.marker = Marker(byte)
        except ValueError as err:
            raise RuntimeError(f"Unknown marker {hex(byte)}") from err
        return default_frame
    else:
        return cls([])
