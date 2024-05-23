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
        mname = super().__getattribute__("name")
        attrs = {
            "__spec__": None,
            "__name__": mname,
            "__class__": None,
            "__path__": None,
        }
        if name in attrs:
            return attrs[name]
        attr = getattr(assets, name)
        if not callable(attr):
            return attr
        return partial(attr, mname)
