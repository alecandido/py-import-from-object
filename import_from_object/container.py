import importlib
import importlib.util
import sys
from functools import partial

from . import assets


def register(name, obj):
    # prevent overwriting existing modules
    if name in sys.modules:
        raise ValueError(
            f"Module '{name}' already present. "
            "Choose a different one to avoid overwriting it."
        )

    # allow relative paths, where relative is intended respect to package root
    root = __name__.split(".")[0]
    qualified = importlib.util.resolve_name(name, root)

    # allow to nest module in arbitrary subpackage
    if "." in qualified:
        parent_name, _, child_name = qualified.rpartition(".")
        parent_module = importlib.import_module(parent_name)
        setattr(parent_module, child_name, obj)

    sys.modules[qualified] = obj
    obj.name = obj.__name__ = qualified
    obj.__spec__ = None


class ModuleContainer:
    def __init__(self, name: str) -> None:
        register(name, self)

    def __getattribute__(self, name: str):
        try:
            if name.startswith("_"):
                raise AttributeError

            attr = getattr(assets, name)
            if not callable(attr):
                return attr
            return partial(attr, self.name)
        except AttributeError:
            return super().__getattribute__(name)
