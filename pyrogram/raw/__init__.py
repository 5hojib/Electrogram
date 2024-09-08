from __future__ import annotations

from importlib import import_module

from . import base, core, functions, types
from .all import objects

for k, v in objects.items():
    path, name = v.rsplit(".", 1)
    objects[k] = getattr(import_module(path), name)

__all__ = ["base", "core", "functions", "objects", "types"]
