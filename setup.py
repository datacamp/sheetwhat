#!/usr/bin/env python

import re
import ast
from os import path
from setuptools import setup

_version_re = re.compile(r"__version__\s+=\s+(.*)")

PACKAGE_NAME = "sheetwhat"
REQUIREMENT_NAMES = ["protowhat", "glom"]

HERE = path.abspath(path.dirname(__file__))
with open(path.join(HERE, "README.md"), encoding="utf-8") as fp:
    README = fp.read()
with open(path.join(HERE, PACKAGE_NAME, '__init__.py'), encoding="utf-8") as fp:
    _version_re = re.compile(r"__version__\s+=\s+(.*)")
    VERSION = str(ast.literal_eval(_version_re.search(
        fp.read()).group(1)))
with open(path.join(HERE, "requirements.txt"), encoding="utf-8") as fp:
    req_txt = fp.read()
    _requirements_re_template = r"^({}[\s<>=]*.*)$"
    REQUIREMENTS = [
        re.search(_requirements_re_template.format(requirement), req_txt, re.M).group(0)
        for requirement in REQUIREMENT_NAMES
    ]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    packages=["sheetwhat", "sheetwhat.checks"],
    install_requires=REQUIREMENTS,
    description="Submission correctness tests for spreadsheets",
    long_description=README,
    long_description_content_type="text/markdown",
    license="GNU version 3",
    author="Vincent Vankrunkelsven",
    author_email="vincent@datacamp.com",
    maintainer="Jeroen Hermans",
    maintainer_email="content-engineering@datacamp.com",
    url="https://github.com/datacamp/sheetwhat",
)
