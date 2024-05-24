import sys
from functools import partial

from . import assets


class ModuleContainer:
    def __init__(self, name) -> None:
        self.name = name
        if name in sys.modules:
            raise ValueError(
                f"Module '{name}' already present. "
                "Choose a different one to avoid overwriting it."
            )
        sys.modules[name] = self

    def __getattribute__(self, name):
        attrs = {
            "__spec__": None,
            "__name__": super().__getattribute__("name"),
        }

        try:
            return attrs[name]
        except KeyError:
            pass
        try:
            attr = getattr(assets, name)
            if not callable(attr):
                return attr
            return partial(attr, self.name)
        except AttributeError:
            return super().__getattribute__(name)
