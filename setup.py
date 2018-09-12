#!/usr/bin/env python3


# @Author: George Onoufriou <archer>
# @Date:   2018-09-05
# @Filename: setup.py
# @Last modified by:   archer
# @Last modified time: 2018-09-12
# @License: Please see LICENSE file in project root

import subprocess as sp
from setuptools import setup, find_packages, find_namespace_packages


# getting version from git as this is vcs
runArgs = ["git", "describe", "--long"]
version = sp.run(runArgs, stdout=sp.PIPE).stdout.decode("utf-8")

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="nemesyst",
    version=str(version),
    description="Generalised, sequence-based, deep-learning framework of the gods. Warning may include GANs, does not include nuts.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="George Onoufriou",
    url="https://github.com/DreamingRaven/Nemesyst",
    packages=find_namespace_packages(),
    scripts=['nemesyst.py'],
)
