import re
from sys import argv
from setuptools import setup, find_packages
from compiler.api import compiler as api_compiler
from compiler.errors import compiler as errors_compiler


requires = [
    "aiosqlite",
    "pymediainfo==6.0.1",
    "pymongo==4.4.1",
    "pysocks",
    "tgcrypto"
]

if len(argv) > 1 and argv[1] in ["bdist_wheel", "install", "develop"]:
    api_compiler.start()
    errors_compiler.start()

setup(
    name="pyrogram",
    version="v1.181.0",
    author="5hojib",
    author_email="yesiamshojib@gmail.com",
    description="Nothing",
    long_description="Nothing",
    long_description_content_type="text/markdown",
    url="https://github.com/5hojib/pyrogram",
    python_requires="~=3.8",
    package_data={
        "pyrogram": ["py.typed"],
    },
    packages=find_packages(exclude=["compiler*"]),
    zip_safe=False,
    install_requires=requires
)
