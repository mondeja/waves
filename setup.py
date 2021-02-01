#!/usr/bin/env python
# -*- coding: utf-8 -*-

import io
import os
import re

from setuptools import find_packages, setup


URL = "https://github.com/mondeja/waves"
EMAIL = "mondejar1994@gmail.com"
AUTHOR = "Álvaro Mondéjar Rubio"

REQUIRES_PYTHON = ">=3"
REQUIRED = [
    "pysndfile",
    "numpy",
    "matplotlib",
    "pygame",
]
LINT_EXTRAS = [
    "flake8==3.8.4",
    "flake8-absolute-import>=1.0",
    "flake8-implicit-str-concat==0.2.0",
    "flake8-print==4.0.0",
    "isort==5.7.0",
    "black",
    "yamllint==1.26.0",
]
TEST_EXTRAS = [
    "pytest==6.2.2",
    "pytest-cov==2.10.1",
]
DOC_EXTRAS = [
    "Sphinx==3.4.3",
    "furo==2020.12.30b24",
]
DEV_EXTRAS = (
    [
        "bump2version==1.0.1",
        "pre-commit==2.9.3",
    ]
    + DOC_EXTRAS
    + TEST_EXTRAS
    + LINT_EXTRAS
)

HERE = os.path.abspath(os.path.dirname(__file__))

with io.open(os.path.join(HERE, "README.rst"), encoding="utf-8") as f:
    LONG_DESCRIPTION = "\n" + f.read()

ABOUT = {}
INIT_FILEPATH = os.path.join(HERE, "waves", "__init__.py")
with io.open(INIT_FILEPATH, encoding="utf-8") as f:
    content = f.read()
    ABOUT["__title__"] = re.search(r"__title__\s=\s[\"']([^\"']+)[\"']", content).group(
        1
    )
    ABOUT["__version__"] = re.search(
        r"__version__\s=\s[\"']([^\"']+)[\"']", content
    ).group(1)
    ABOUT["__description__"] = re.search(
        r"__description__\s=\s[\"']([^\"']+)[\"']", content
    ).group(1)

setup(
    name=ABOUT["__title__"],
    version=ABOUT["__version__"],
    description=ABOUT["__description__"],
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(exclude=["tests"]),
    install_requires=REQUIRED,
    extras_require={
        "dev": DEV_EXTRAS,
        "test": TEST_EXTRAS,
        "lint": LINT_EXTRAS,
        "doc": DOC_EXTRAS,
    },
    include_package_data=True,
    license="BSD License",
    classifiers=[
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
)
