from __future__ import annotations

import ast
import os
import re
import shutil
from .vao import methods_all, types_all, b_all

HOME = "compiler/docs"
DESTINATION = "docs/source/telegram"
PYROGRAM_API_DEST = "docs/source/api"

FUNCTIONS_PATH = "pyrogram/raw/functions"
TYPES_PATH = "pyrogram/raw/types"
BASE_PATH = "pyrogram/raw/base"

FUNCTIONS_BASE = "functions"
TYPES_BASE = "types"
BASE_BASE = "base"


def snek(s: str):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def generate(source_path, base):
    all_entities = {}

    def build(path, level=0):
        last = path.split("/")[-1]

        for i in os.listdir(path):
            try:
                if not i.startswith("__"):
                    build("/".join([path, i]), level=level + 1)
            except NotADirectoryError:
                with open(path + "/" + i, encoding="utf-8") as f:
                    p = ast.parse(f.read())

                for node in ast.walk(p):
                    if isinstance(node, ast.ClassDef):
                        name = node.name
                        break
                else:
                    continue

                full_path = (
                    os.path.basename(path)
                    + "/"
                    + snek(name).replace("_", "-")
                    + ".rst"
                )

                if level:
                    full_path = base + "/" + full_path

                namespace = path.split("/")[-1]
                if namespace in ["base", "types", "functions"]:
                    namespace = ""

                full_name = f"{(namespace + '.') if namespace else ''}{name}"

                os.makedirs(
                    os.path.dirname(DESTINATION + "/" + full_path), exist_ok=True
                )

                with open(DESTINATION + "/" + full_path, "w", encoding="utf-8") as f:
                    f.write(
                        page_template.format(
                            title=full_name,
                            title_markup="=" * len(full_name),
                            full_class_path="pyrogram.raw.{}".format(
                                ".".join(full_path.split("/")[:-1]) + "." + name
                            ),
                        )
                    )

                if last not in all_entities:
                    all_entities[last] = []

                all_entities[last].append(name)

    build(source_path)

    for k, v in sorted(all_entities.items()):
        v = sorted(v)
        entities = []

        for i in v:
            entities.append(f'{i} <{snek(i).replace("_", "-")}>')

        if k != base:
            inner_path = base + "/" + k + "/index" + ".rst"
            module = f"pyrogram.raw.{base}.{k}"
        else:
            for i in sorted(all_entities, reverse=True):
                if i != base:
                    entities.insert(0, f"{i}/index")

            inner_path = base + "/index" + ".rst"
            module = f"pyrogram.raw.{base}"

        with open(DESTINATION + "/" + inner_path, "w", encoding="utf-8") as f:
            if k == base:
                f.write(":tocdepth: 1\n\n")
                k = "Raw " + k

            f.write(
                toctree.format(
                    title=k.title(),
                    title_markup="=" * len(k),
                    module=module,
                    entities="\n    ".join(entities),
                )
            )

            f.write("\n")


def pyrogram_api():
    def get_title_list(s: str) -> list:
        return [i.strip() for i in [j.strip() for j in s.split("\n") if j] if i]


    root = PYROGRAM_API_DEST + "/methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in methods_all.items():
            name, *methods = get_title_list(v)
            fmt_keys.update({k: "\n    ".join(f"{m} <{m}>" for m in methods)})

            for method in methods:
                with open(root + f"/{method}.rst", "w") as f2:
                    title = f"{method}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. automethod:: pyrogram.Client.{method}()")

            functions = ["idle", "compose"]

            for func in functions:
                with open(root + f"/{func}.rst", "w") as f2:
                    title = f"{func}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. autofunction:: pyrogram.{func}()")

        f.write(template.format(**fmt_keys))


    root = PYROGRAM_API_DEST + "/types"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/types.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in types_all.items():
            name, *types = get_title_list(v)

            fmt_keys.update({k: "\n    ".join(types)})

            for type in types:
                with open(root + f"/{type}.rst", "w") as f2:
                    title = f"{type}"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. autoclass:: pyrogram.types.{type}()\n")

        f.write(template.format(**fmt_keys))


    root = PYROGRAM_API_DEST + "/bound-methods"

    shutil.rmtree(root, ignore_errors=True)
    os.mkdir(root)

    with open(HOME + "/template/bound-methods.rst") as f:
        template = f.read()

    with open(root + "/index.rst", "w") as f:
        fmt_keys = {}

        for k, v in b_all.items():
            name, *bound_methods = get_title_list(v)

            fmt_keys.update(
                {
                    f"{k}_hlist": "\n    ".join(
                        f"- :meth:`~{bm}`" for bm in bound_methods
                    )
                }
            )

            fmt_keys.update(
                {
                    f"{k}_toctree": "\n    ".join(
                        "{} <{}>".format(bm.split(".")[1], bm)
                        for bm in bound_methods
                    )
                }
            )

            for bm in bound_methods:
                with open(root + f"/{bm}.rst", "w") as f2:
                    title = f"{bm}()"

                    f2.write(title + "\n" + "=" * len(title) + "\n\n")
                    f2.write(f".. automethod:: pyrogram.types.{bm}()")

        f.write(template.format(**fmt_keys))


def start():
    global page_template
    global toctree

    shutil.rmtree(DESTINATION, ignore_errors=True)

    with open(HOME + "/template/page.txt", encoding="utf-8") as f:
        page_template = f.read()

    with open(HOME + "/template/toctree.txt", encoding="utf-8") as f:
        toctree = f.read()

    generate(TYPES_PATH, TYPES_BASE)
    generate(FUNCTIONS_PATH, FUNCTIONS_BASE)
    generate(BASE_PATH, BASE_BASE)
    pyrogram_api()


if __name__ == "__main__":
    FUNCTIONS_PATH = "../../pyrogram/raw/functions"
    TYPES_PATH = "../../pyrogram/raw/types"
    BASE_PATH = "../../pyrogram/raw/base"
    HOME = "."
    DESTINATION = "../../docs/source/telegram"
    PYROGRAM_API_DEST = "../../docs/source/api"

    start()
