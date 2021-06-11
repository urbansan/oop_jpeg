from ..utils import get_subclasses
from .abstract import AbstractFrame
from .markers import Marker
from ._frames import DefaultFrame


factory_dict = {}

for marker in Marker:
    factory_dict[marker.value] = DefaultFrame

for cls in get_subclasses(AbstractFrame):
    factory_dict[cls.marker] = cls
