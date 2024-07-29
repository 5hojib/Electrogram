import contextlib
import re
import shutil
from functools import partial
from pathlib import Path
from typing import NamedTuple

API_HOME_PATH = Path(__file__).parent.resolve()
REPO_HOME_PATH = API_HOME_PATH.parent.parent

DESTINATION_PATH = REPO_HOME_PATH / "pyrogram" / "raw"


SECTION_RE = re.compile(r"---(\w+)---")
LAYER_RE = re.compile(r"//\sLAYER\s(\d+)")
COMBINATOR_RE = re.compile(
    r"^([\w.]+)#([0-9a-f]+)\s(?:.*)=\s([\w<>.]+);$", re.MULTILINE
)
ARGS_RE = re.compile(r"[^{](\w+):([\w?!.<>#]+)")
FLAGS_RE = re.compile(r"flags(\d?)\.(\d+)\?")
FLAGS_RE_2 = re.compile(r"flags(\d?)\.(\d+)\?([\w<>.]+)")
FLAGS_RE_3 = re.compile(r"flags(\d?):#")
INT_RE = re.compile(r"int(\d+)")

CORE_TYPES = [
    "int",
    "long",
    "int128",
    "int256",
    "double",
    "bytes",
    "string",
    "Bool",
    "true",
]
open = partial(open, encoding="utf-8")

types_to_constructors: dict[str, list[str]] = {}
types_to_functions: dict[str, list[str]] = {}
constructors_to_functions: dict[str, list[str]] = {}
namespaces_to_types: dict[str, list[str]] = {}
namespaces_to_constructors: dict[str, list[str]] = {}
namespaces_to_functions: dict[str, list[str]] = {}


class Combinator(NamedTuple):
    section: str
    qualname: str
    namespace: str
    name: str
    id: str
    has_flags: bool
    args: list[tuple[str, str]]
    qualtype: str
    typespace: str
    type: str


def snake(s: str):
    # https://stackoverflow.com/q/1175208
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def camel(s: str):
    return "".join(i[0].upper() + i[1:] for i in s.split("_"))


def get_type_hint(type: str) -> str:
    is_flag = FLAGS_RE.match(type)
    is_core = False

    if is_flag:
        type = type.split("?")[1]

    if type in CORE_TYPES:
        is_core = True

        if type == "long" or "int" in type:
            type = "int"
        elif type == "double":
            type = "float"
        elif type == "string":
            type = "str"
        elif type in {"Bool", "true"}:
            type = "bool"
        else:  # bytes and object
            type = "bytes"

    if type in {"Object", "!X"}:
        return "TLObject"

    if re.match("^vector", type, re.IGNORECASE):
        is_core = True

        sub_type = type.split("<")[1][:-1]
        type = f"List[{get_type_hint(sub_type)}]"

    if is_core:
        return f"Optional[{type}] = None" if is_flag else type
    ns, name = type.split(".") if "." in type else ("", type)
    type = '"raw.base.' + ".".join([ns, name]).strip(".") + '"'

    return f'{type}{" = None" if is_flag else ""}'


def sort_args(args: list[tuple[str, str]]):
    """Put flags at the end"""
    args = args.copy()
    flags = [i for i in args if FLAGS_RE.match(i[1])]

    for i in flags:
        args.remove(i)

    for i in args[:]:
        if re.match(r"flags\d?", i[0]) and i[1] == "#":
            args.remove(i)

    return args + flags


def remove_whitespaces(source: str) -> str:
    """Remove whitespaces from blank lines"""
    lines = source.split("\n")

    for i, _ in enumerate(lines):
        if re.match(r"^\s+$", lines[i]):
            lines[i] = ""

    return "\n".join(lines)


def start(format: bool = False) -> None:
    shutil.rmtree(DESTINATION_PATH / "types", ignore_errors=True)
    shutil.rmtree(DESTINATION_PATH / "functions", ignore_errors=True)
    shutil.rmtree(DESTINATION_PATH / "base", ignore_errors=True)

    with (
        open(API_HOME_PATH / "source/auth_key.tl") as f1,
        open(API_HOME_PATH / "source/sys_msgs.tl") as f2,
        open(API_HOME_PATH / "source/main_api.tl") as f3,
    ):
        schema = (f1.read() + f2.read() + f3.read()).splitlines()

    with (
        open(API_HOME_PATH / "template/type.txt") as f1,
        open(API_HOME_PATH / "template/combinator.txt") as f2,
    ):
        type_tmpl = f1.read()
        combinator_tmpl = f2.read()

    layer = None
    combinators: list[Combinator] = []

    section = None
    for line in schema:
        if section_match := SECTION_RE.match(line):
            section = section_match.group(1)
            continue

        if layer_match := LAYER_RE.match(line):
            layer = layer_match.group(1)
            continue

        if combinator_match := COMBINATOR_RE.match(line):
            qualname, id, qualtype = combinator_match.groups()

            namespace, name = (
                qualname.split(".")
                if "." in qualname
                else ("", qualname)
            )
            name = camel(name)
            qualname = ".".join([namespace, name]).lstrip(".")

            typespace, type = (
                qualtype.split(".")
                if "." in qualtype
                else ("", qualtype)
            )
            type = camel(type)
            qualtype = ".".join([typespace, type]).lstrip(".")

            has_flags = bool(FLAGS_RE_3.findall(line))

            args = ARGS_RE.findall(line)

            # Fix arg name being "self" or "from" (reserved python keywords)
            for i, item in enumerate(args):
                if item[0] == "self":
                    args[i] = ("is_self", item[1])
                if item[0] == "from":
                    args[i] = ("from_peer", item[1])

            combinator = Combinator(
                section=section,
                qualname=qualname,
                namespace=namespace,
                name=name,
                id=f"0x{id}",
                has_flags=has_flags,
                args=args,
                qualtype=qualtype,
                typespace=typespace,
                type=type,
            )

            combinators.append(combinator)

    for c in combinators:
        qualtype = c.qualtype

        if qualtype.startswith("Vector"):
            qualtype = qualtype.split("<")[1][:-1]

        d = (
            types_to_constructors
            if c.section == "types"
            else types_to_functions
        )

        if qualtype not in d:
            d[qualtype] = []

        d[qualtype].append(c.qualname)

        if c.section == "types":
            key = c.namespace

            if key not in namespaces_to_types:
                namespaces_to_types[key] = []

            if c.type not in namespaces_to_types[key]:
                namespaces_to_types[key].append(c.type)

    for k, v in types_to_constructors.items():
        for i in v:
            with contextlib.suppress(KeyError):
                constructors_to_functions[i] = types_to_functions[k]

    for qualtype, qualval in types_to_constructors.items():
        typespace, type = (
            qualtype.split(".") if "." in qualtype else ("", qualtype)
        )
        dir_path = DESTINATION_PATH / "base" / typespace

        module = type

        if module == "Updates":
            module = "UpdatesT"

        dir_path.mkdir(parents=True, exist_ok=True)

        constructors = sorted(qualval)
        len(constructors)
        "\n            ".join([f"{c}" for c in constructors])

        with open(dir_path / f"{snake(module)}.py", "w") as f:
            f.write(
                type_tmpl.format(
                    name=type,
                    qualname=qualtype,
                    types=", ".join(
                        [f'"raw.types.{c}"' for c in constructors]
                    ),
                    doc_name=snake(type).replace("_", "-"),
                )
            )

    for c in combinators:
        sorted_args = sort_args(c.args)

        arguments = (", *, " if c.args else "") + (
            ", ".join(
                [
                    f"{i[0]}: {get_type_hint(i[1])}"
                    for i in sorted_args
                ]
            )
            if sorted_args
            else ""
        )

        fields = (
            "\n        ".join(
                [
                    f"self.{i[0]} = {i[0]}  # {i[1]}"
                    for i in sorted_args
                ]
            )
            if sorted_args
            else "pass"
        )

        for arg in sorted_args:
            arg_name, arg_type = arg
            FLAGS_RE.match(arg_type)
            arg_type = arg_type.split("?")[-1]

        write_types = read_types = (
            "" if c.has_flags else "# No flags\n        "
        )

        for arg_name, arg_type in c.args:
            flag = FLAGS_RE_2.match(arg_type)

            if re.match(r"flags\d?", arg_name) and arg_type == "#":
                write_flags = []

                for i in c.args:
                    flag = FLAGS_RE_2.match(i[1])

                    if flag:
                        if arg_name != f"flags{flag.group(1)}":
                            continue

                        if flag.group(3) == "true" or flag.group(
                            3
                        ).startswith("Vector"):
                            write_flags.append(
                                f"{arg_name} |= (1 << {flag.group(2)}) if self.{i[0]} else 0"
                            )
                        else:
                            write_flags.append(
                                f"{arg_name} |= (1 << {flag.group(2)}) if self.{i[0]} is not None else 0"
                            )

                write_flags = "\n        ".join(
                    [
                        f"{arg_name} = 0",
                        "\n        ".join(write_flags),
                        f"b.write(Int({arg_name}))\n        ",
                    ]
                )

                write_types += write_flags
                read_types += (
                    f"\n        {arg_name} = Int.read(b)\n        "
                )

                continue

            if flag:
                number, index, flag_type = flag.groups()

                if flag_type == "true":
                    read_types += "\n        "
                    read_types += f"{arg_name} = True if flags{number} & (1 << {index}) else False"
                elif flag_type in CORE_TYPES:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f"b.write({flag_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {flag_type.title()}.read(b) if flags{number} & (1 << {index}) else None"
                elif "vector" in flag_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += f'b.write(Vector(self.{arg_name}{f", {sub_type.title()}" if sub_type in CORE_TYPES else ""}))\n        '

                    read_types += "\n        "
                    read_types += f'{arg_name} = TLObject.read(b{f", {sub_type.title()}" if sub_type in CORE_TYPES else ""}) if flags{number} & (1 << {index}) else []\n        '
                else:
                    write_types += "\n        "
                    write_types += f"if self.{arg_name} is not None:\n            "
                    write_types += (
                        f"b.write(self.{arg_name}.write())\n        "
                    )

                    read_types += "\n        "
                    read_types += f"{arg_name} = TLObject.read(b) if flags{number} & (1 << {index}) else None\n        "
            else:
                write_types += "\n        "
                if arg_type in CORE_TYPES:
                    write_types += f"b.write({arg_type.title()}(self.{arg_name}))\n        "

                    read_types += "\n        "
                    read_types += f"{arg_name} = {arg_type.title()}.read(b)\n        "
                elif "vector" in arg_type.lower():
                    sub_type = arg_type.split("<")[1][:-1]

                    write_types += f'b.write(Vector(self.{arg_name}{f", {sub_type.title()}" if sub_type in CORE_TYPES else ""}))\n        '

                    read_types += "\n        "
                    read_types += f'{arg_name} = TLObject.read(b{f", {sub_type.title()}" if sub_type in CORE_TYPES else ""})\n        '
                else:
                    write_types += (
                        f"b.write(self.{arg_name}.write())\n        "
                    )

                    read_types += "\n        "
                    read_types += (
                        f"{arg_name} = TLObject.read(b)\n        "
                    )

        slots = ", ".join([f'"{i[0]}"' for i in sorted_args])
        return_arguments = ", ".join(
            [f"{i[0]}={i[0]}" for i in sorted_args]
        )

        compiled_combinator = combinator_tmpl.format(
            name=c.name,
            slots=slots,
            id=c.id,
            qualname=f"{c.section}.{c.qualname}",
            arguments=arguments,
            fields=fields,
            read_types=read_types,
            write_types=write_types,
            return_arguments=return_arguments,
        )

        directory = "types" if c.section == "types" else c.section

        dir_path = DESTINATION_PATH / directory / c.namespace

        dir_path.mkdir(exist_ok=True, parents=True)

        module = c.name

        if module == "Updates":
            module = "UpdatesT"

        with open(dir_path / f"{snake(module)}.py", "w") as f:
            f.write(compiled_combinator)

        d = (
            namespaces_to_constructors
            if c.section == "types"
            else namespaces_to_functions
        )

        if c.namespace not in d:
            d[c.namespace] = []

        d[c.namespace].append(c.name)

    for namespace, types in namespaces_to_types.items():
        with open(
            DESTINATION_PATH / "base" / namespace / "__init__.py", "w"
        ) as f:
            all = []

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                all.append(t)

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_types))}"
                )

            all.extend(filter(bool, namespaces_to_types))

            f.write("\n\n__all__ = [\n")
            for it in all:
                f.write(f'    "{it}",\n')
            f.write("]\n")

    for namespace, types in namespaces_to_constructors.items():
        with open(
            DESTINATION_PATH / "types" / namespace / "__init__.py",
            "w",
        ) as f:
            all = []

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                all.append(t)

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_constructors))}\n"
                )

            all.extend(filter(bool, namespaces_to_constructors))

            f.write("\n\n__all__ = [\n")
            for it in all:
                f.write(f'    "{it}",\n')
            f.write("]\n")

    for namespace, types in namespaces_to_functions.items():
        with open(
            DESTINATION_PATH
            / "functions"
            / namespace
            / "__init__.py",
            "w",
        ) as f:
            all = []

            for t in types:
                module = t

                if module == "Updates":
                    module = "UpdatesT"

                all.append(t)

                f.write(f"from .{snake(module)} import {t}\n")

            if not namespace:
                f.write(
                    f"from . import {', '.join(filter(bool, namespaces_to_functions))}"
                )

            all.extend(filter(bool, namespaces_to_functions))

            f.write("\n\n__all__ = [\n")
            for it in all:
                f.write(f'    "{it}",\n')
            f.write("]\n")

    with open(
        DESTINATION_PATH / "all.py", "w", encoding="utf-8"
    ) as f:
        f.write(f"layer = {layer}\n\n")
        f.write("objects = {")

        for c in combinators:
            f.write(
                f'\n    {c.id}: "pyrogram.raw.{c.section}.{c.qualname}",'
            )

        f.write('\n    0xbc799737: "pyrogram.raw.core.BoolFalse",')
        f.write('\n    0x997275b5: "pyrogram.raw.core.BoolTrue",')
        f.write('\n    0x1cb5c415: "pyrogram.raw.core.Vector",')
        f.write('\n    0x73f1f8dc: "pyrogram.raw.core.MsgContainer",')
        f.write('\n    0xae500895: "pyrogram.raw.core.FutureSalts",')
        f.write('\n    0x0949d9dc: "pyrogram.raw.core.FutureSalt",')
        f.write('\n    0x3072cfa1: "pyrogram.raw.core.GzipPacked",')
        f.write('\n    0x5bb8e511: "pyrogram.raw.core.Message",')

        f.write("\n}\n")


if __name__ == "__main__":
    start(format=False)
