# ruff: noqa: ARG002
from __future__ import annotations

from enum import Enum


class AutoName(Enum):
    def _generate_next_value_(self, *args):
        return self.lower()

    def __repr__(self) -> str:
        return f"pyrogram.enums.{self}"
