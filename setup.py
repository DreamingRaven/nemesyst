#!/usr/bin/env python3


# @Author: George Onoufriou <archer>
# @Date:   2018-09-05
# @Filename: setup.py
# @Last modified by:   archer
# @Last modified time: 2019-07-15
# @License: Please see LICENSE file in project root

import subprocess
from setuptools import setup, find_packages, find_namespace_packages


# getting version from git as this is vcs
# git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g
git_describe = subprocess.Popen(["git", "describe", "--long"],
                                stdout=subprocess.PIPE)
version_num = subprocess.check_output(["sed", r"s/\([^-]*-\)g/r\1/;s/-/./g"],
                                      stdin=git_describe.stdout)
git_describe.wait()
version_git = version_num.decode("ascii").strip()

with open("README.md", "r") as fh:
    readme = fh.read()

setup(
    name="nemesyst",
    version=str(version_git),
    description="Generalised, sequence-based, deep-learning framework of the" +
                "gods. Warning may include GANs, does not include nuts.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="George Onoufriou",
    url="https://github.com/DreamingRaven/nemesyst",
    packages=find_namespace_packages(),
    scripts=['nemesyst.py'],
)
