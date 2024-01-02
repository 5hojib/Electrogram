import csv
from pathlib import Path

for p in Path("source").glob("*.tsv"):
    with open(p) as f:
        reader = csv.reader(f, delimiter="\t")
        dct = {k: v for k, v in reader if k != "id"}
        keys = sorted(dct)

    with open(p, "w") as f:
        f.write("id\tmessage\n")

        for i, item in enumerate(keys, start=1):
            f.write(f"{item}\t{dct[item]}")

            if i != len(keys):
                f.write("\n")
