# ruff: noqa: ARG002
from __future__ import annotations

import sys

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

sys.path.insert(0, ".")


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data) -> None:
        if self.target_name not in {"wheel", "install"}:
            return

        from compiler.api.compiler import start as compile_api
        from compiler.errors.compiler import start as compile_errors

        compile_api()
        compile_errors()
