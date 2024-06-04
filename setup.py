from setuptools import setup, find_packages
from compiler.api import compiler as api_compiler
from compiler.errors import compiler as errors_compiler


with open("requirements.txt", encoding="utf-8") as r:
    requires = [i.strip() for i in r]

api_compiler.start()
errors_compiler.start()

setup(
    name="pyrogram",
    version="v1.181.0",
    author="5hojib",
    author_email="yesiamshojib@gmail.com",
    description="A simple fork of pyrogram",
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
