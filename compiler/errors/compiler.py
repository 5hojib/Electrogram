import csv
import os
import re
import shutil
from pathlib import Path

ERRORS_HOME_PATH = Path(__file__).parent.resolve()
REPO_HOME_PATH = ERRORS_HOME_PATH.parent.parent

ERRORS_DEST_PATH = (
    REPO_HOME_PATH / "pyrogram" / "errors" / "exceptions"
)


def snake(s):
    # https://stackoverflow.com/questions/1175208/elegant-python-function-to-convert-camelcase-to-snake-case
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def camel(s):
    s = snake(s).split("_")
    return "".join(str(i.title()) for i in s)


def start() -> None:
    shutil.rmtree(ERRORS_DEST_PATH, ignore_errors=True)
    ERRORS_DEST_PATH.mkdir(parents=True)

    files = os.listdir(f"{ERRORS_HOME_PATH}/source")

    with (ERRORS_DEST_PATH / "all.py").open(
        "w", encoding="utf-8"
    ) as f_all:
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()

            f_all.write(f"    {code}: {{\n")

            init = ERRORS_DEST_PATH / "__init__.py"

            with init.open("a", encoding="utf-8") as f_init:
                f_init.write(
                    f"from .{name.lower()}_{code} import *\n"
                )

            with (
                (ERRORS_HOME_PATH / "source" / i).open(
                    encoding="utf-8"
                ) as f_csv,
                (ERRORS_DEST_PATH / f"{name.lower()}_{code}.py").open(
                    "w", encoding="utf-8"
                ) as f_class,
            ):
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = camel(name)
                name = " ".join(
                    [
                        i.capitalize()
                        for i in re.sub(r"_", " ", name)
                        .lower()
                        .split(" ")
                    ]
                )

                sub_classes = []

                f_all.write(f'        "_": "{super_class}",\n')

                for j, row in enumerate(reader):
                    if j == 0:
                        continue

                    count += 1

                    if not row:  # Row is empty (blank line)
                        continue

                    error_id, error_message = row

                    sub_class = camel(re.sub(r"_X", "_", error_id))
                    sub_class = re.sub(r"^2", "Two", sub_class)
                    sub_class = re.sub(r" ", "", sub_class)

                    f_all.write(
                        f'        "{error_id}": "{sub_class}",\n'
                    )

                    sub_classes.append(
                        (sub_class, error_id, error_message)
                    )

                with (
                    ERRORS_HOME_PATH / "template" / "class.txt"
                ).open(encoding="utf-8") as f_class_template:
                    class_template = f_class_template.read()

                    with (
                        ERRORS_HOME_PATH
                        / "template"
                        / "sub_class.txt"
                    ).open(encoding="utf-8") as f_sub_class_template:
                        sub_class_template = (
                            f_sub_class_template.read()
                        )

                    class_template = class_template.format(
                        super_class=super_class,
                        code=code,
                        sub_classes="".join(
                            [
                                sub_class_template.format(
                                    sub_class=k[0],
                                    super_class=super_class,
                                    id=f'"{k[1]}"',
                                )
                                for k in sub_classes
                            ]
                        ),
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with (ERRORS_DEST_PATH / "all.py").open(encoding="utf-8") as f:
        content = f.read()

    with (ERRORS_DEST_PATH / "all.py").open(
        "w", encoding="utf-8"
    ) as f:
        f.write(re.sub("{count}", str(count), content))


if __name__ == "__main__":
    start()
