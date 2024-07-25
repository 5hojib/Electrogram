import csv
import os
import re
import shutil

HOME = "compiler/errors"
DEST = "pyrogram/errors/exceptions"


def snek(s):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def caml(s):
    s = snek(s).split("_")
    return "".join([str(i.title()) for i in s])


def start():
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST)

    files = [i for i in os.listdir(f"{HOME}/source")]

    with open(f"{DEST}/all.py", "w", encoding="utf-8") as f_all:
        f_all.write("\n\n")
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()

            f_all.write(f"    {code}: {{\n")

            init = f"{DEST}/__init__.py"

            if not os.path.exists(init):
                with open(init, "w", encoding="utf-8") as f_init:
                    f_init.write("\n\n")

            with open(init, "a", encoding="utf-8") as f_init:
                f_init.write(f"from .{name.lower()}_{code} import *\n")

            with open(f"{HOME}/source/{i}", encoding="utf-8") as f_csv, open(
                f"{DEST}/{name.lower()}_{code}.py", "w", encoding="utf-8"
            ) as f_class:
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = caml(name)
                name = " ".join(
                    [
                        str(i.capitalize())
                        for i in re.sub(r"_", " ", name).lower().split(" ")
                    ]
                )

                sub_classes = []

                f_all.write(f'        "_": "{super_class}",\n')

                for j, row in enumerate(reader):
                    if j == 0:
                        continue

                    count += 1

                    if not row:
                        continue

                    error_id, error_message = row

                    sub_class = caml(re.sub(r"_X", "_", error_id))
                    sub_class = re.sub(r"^2", "Two", sub_class)
                    sub_class = re.sub(r" ", "", sub_class)

                    f_all.write(f'        "{error_id}": "{sub_class}",\n')

                    sub_classes.append((sub_class, error_id, error_message))

                with open(
                    f"{HOME}/template/class.txt", encoding="utf-8"
                ) as f_class_template:
                    class_template = f_class_template.read()

                    with open(
                        f"{HOME}/template/sub_class.txt", encoding="utf-8"
                    ) as f_sub_class_template:
                        sub_class_template = f_sub_class_template.read()

                    class_template = class_template.format(
                        super_class=super_class,
                        code=code,
                        docstring=f'"""{name}"""',
                        sub_classes="".join(
                            [
                                sub_class_template.format(
                                    sub_class=k[0],
                                    super_class=super_class,
                                    id=f'"{k[1]}"',
                                    docstring=f'"""{k[2]}"""',
                                )
                                for k in sub_classes
                            ]
                        ),
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with open(f"{DEST}/all.py", encoding="utf-8") as f:
        content = f.read()

    with open(f"{DEST}/all.py", "w", encoding="utf-8") as f:
        f.write(re.sub("{count}", str(count), content))


if "__main__" == __name__:
    HOME = "."
    DEST = "../../pyrogram/errors/exceptions"

    start()
