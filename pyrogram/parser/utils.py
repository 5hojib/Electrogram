from __future__ import annotations

import re
from struct import unpack

# SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")


def add_surrogates(text):
    # Replace each SMP code point with a surrogate pair
    return SMP_RE.sub(
        lambda match:  # Split SMP in two surrogates
        "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))),
        text,
    )


def remove_surrogates(text):
    # Replace each surrogate pair with a SMP code point
    return text.encode("utf-16", "surrogatepass").decode("utf-16")


def replace_once(source: str, old: str, new: str, start: int):
    return source[:start] + source[start:].replace(old, new, 1)
