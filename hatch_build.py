import sys

from hatchling.builders.hooks.plugin.interface import BuildHookInterface

sys.path.insert(0, ".")


class CustomHook(BuildHookInterface):
    def initialize(self, version, build_data):
        if self.target_name not in {"wheel", "install"}:
            return

        from compiler.api.compiler import start as compile_api  # noqa: PLC0415
        from compiler.errors.compiler import start as compile_errors  # noqa: PLC0415

        compile_api()
        compile_errors()
