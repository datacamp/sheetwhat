#!/usr/bin/env python

import re
import ast
from os import path
from setuptools import setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

PACKAGE_NAME = "sheetwhat"
HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.md"), encoding="utf-8") as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, "__init__.py"), "rb") as fp:
    VERSION = str(
        ast.literal_eval(_version_re.search(fp.read().decode("utf-8")).group(1))
    )

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=["sheetwhat", "sheetwhat.checks"],
    install_requires=["protowhat>=1.1.2", "glom>=18.3.1"],
    description="Submission correctness tests for spreadsheets",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU version 3",
    author="Vincent Vankrunkelsven",
    author_email="vincent@datacamp.com",
    maintainer="Filip Schouwenaars",
    maintainer_email="filip@datacamp.com",
    url="https://github.com/datacamp/sheetwhat",
)
