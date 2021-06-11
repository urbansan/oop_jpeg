from ..utils import get_subclasses
from .abstract import AbstractFrame
from .markers import Marker
from ._frames import DefaultFrame


factory_dict = {}
#
# for marker in Marker:
#     factory_dict[marker.value] = DefaultFrame

for cls in get_subclasses(AbstractFrame):
    factory_dict[cls.marker.value] = cls


def MarkerFactory(byte):
    cls = factory_dict.get(byte)
    if cls is None:
        default_frame = DefaultFrame([])
        try:
            default_frame.marker = Marker(byte)
        except ValueError as err:
            raise RuntimeError(f"Unknown marker {hex(byte)}") from err
        return default_frame
    else:
        return cls([])
