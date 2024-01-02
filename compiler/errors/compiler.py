import csv
import os
import re
import shutil

HOME = "compiler/errors"
DEST = "pyrogram/errors/exceptions"
NOTICE_PATH = "NOTICE"


def snek(s):
    s = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", s)
    return re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s).lower()


def caml(s):
    s = snek(s).split("_")
    return "".join([str(i.title()) for i in s])


def start():
    shutil.rmtree(DEST, ignore_errors=True)
    os.makedirs(DEST)

    files = [i for i in os.listdir("{}/source".format(HOME))]

    with open(NOTICE_PATH, encoding="utf-8") as f:
        notice = []

        for line in f.readlines():
            notice.append("# {}".format(line).strip())

        notice = "\n".join(notice)

    with open("{}/all.py".format(DEST), "w", encoding="utf-8") as f_all:
        f_all.write(notice + "\n\n")
        f_all.write("count = {count}\n\n")
        f_all.write("exceptions = {\n")

        count = 0

        for i in files:
            code, name = re.search(r"(\d+)_([A-Z_]+)", i).groups()

            f_all.write("    {}: {{\n".format(code))

            init = "{}/__init__.py".format(DEST)

            if not os.path.exists(init):
                with open(init, "w", encoding="utf-8") as f_init:
                    f_init.write(notice + "\n\n")

            with open(init, "a", encoding="utf-8") as f_init:
                f_init.write("from .{}_{} import *\n".format(name.lower(), code))

            with open("{}/source/{}".format(HOME, i), encoding="utf-8") as f_csv, \
                open("{}/{}_{}.py".format(DEST, name.lower(), code), "w", encoding="utf-8") as f_class:
                reader = csv.reader(f_csv, delimiter="\t")

                super_class = caml(name)
                name = " ".join([str(i.capitalize()) for i in re.sub(r"_", " ", name).lower().split(" ")])

                sub_classes = []

                f_all.write("        \"_\": \"{}\",\n".format(super_class))

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

                    f_all.write("        \"{}\": \"{}\",\n".format(error_id, sub_class))

                    sub_classes.append((sub_class, error_id, error_message))

                with open("{}/template/class.txt".format(HOME), "r", encoding="utf-8") as f_class_template:
                    class_template = f_class_template.read()

                    with open("{}/template/sub_class.txt".format(HOME), "r", encoding="utf-8") as f_sub_class_template:
                        sub_class_template = f_sub_class_template.read()

                    class_template = class_template.format(
                        notice=notice,
                        super_class=super_class,
                        code=code,
                        docstring='"""{}"""'.format(name),
                        sub_classes="".join([sub_class_template.format(
                            sub_class=k[0],
                            super_class=super_class,
                            id="\"{}\"".format(k[1]),
                            docstring='"""{}"""'.format(k[2])
                        ) for k in sub_classes])
                    )

                f_class.write(class_template)

            f_all.write("    },\n")

        f_all.write("}\n")

    with open("{}/all.py".format(DEST), encoding="utf-8") as f:
        content = f.read()

    with open("{}/all.py".format(DEST), "w", encoding="utf-8") as f:
        f.write(re.sub("{count}", str(count), content))


if "__main__" == __name__:
    HOME = "."
    DEST = "../../pyrogram/errors/exceptions"
    NOTICE_PATH = "../../NOTICE"

    start()
