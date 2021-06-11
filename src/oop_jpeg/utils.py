import importlib
import pkgutil
from pathlib import Path


def get_subclasses(base_cls):
    module = importlib.import_module(base_cls.__module__)
    parent_module_path = Path(module.__file__).parent
    root = str(parent_module_path)

    for importer, module_name, ispkg in pkgutil.iter_modules([root]):
        importlib.import_module(f'.{module_name}', module.__package__)
    classes = base_cls.__subclasses__()
    return classes