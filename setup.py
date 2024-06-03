from setuptools import setup, find_packages
from compiler.api import compiler as api_compiler
from compiler.errors import compiler as errors_compiler


requires = [
    "aiosqlite",
]

api_compiler.start()
errors_compiler.start()

setup(
    name="pyrogram",
    version="v1.181.4",
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
    packages=find_packages(
        exclude=["compiler*"]
    ),
    zip_safe=False,
    install_requires=requires
)
