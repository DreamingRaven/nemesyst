#!/usr/bin/env python3


# @Author: George Onoufriou <archer>
# @Date:   2018-09-05
# @Filename: setup.py
# @Last modified by:   archer
# @Last modified time: 2019-08-17
# @License: Please see LICENSE file in project root

import subprocess
from setuptools import setup, find_packages, find_namespace_packages


def get_gitVersion():
    """Get the version from git describe in archlinux format."""
    try:
        # getting version from git as this is vcs
        # below equivelant or achlinux versioning scheme:
        # git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g
        git_describe = subprocess.Popen(
            ["git", "describe", "--long"],
            stdout=subprocess.PIPE)
        version_num = subprocess.check_output(
            ["sed", r"s/\([^-]*-\)g/r\1/;s/-/./g"],
            stdin=git_describe.stdout)
        git_describe.wait()
        version_git = version_num.decode("ascii").strip()

    except subprocess.CalledProcessError:
        # for those who do not have git or sed availiable (probably non-linux)
        # this is tricky to handle, lots of suggestions exist but none that
        # neither require additional library or subprocessess
        version_git = "0.0.1"  # for now we will provide a number for you
    return version_git


def get_requirements(path=None):
    """get a list of requirements and any dependency links associated.

    This function fascilitates git urls being in requirements.txt
    and installing them as normall just like pip install -r requirements.txt
    would but setup does not by default.
    """
    #  read in the requirements file
    path = path if path is not None else "./requirements.txt"
    with open(path, "r") as f:
        requirements = f.read().splitlines()
    # find and replace all urls with the name of the package being pointed to
    re_git_url = r"^\bgit.+\.git"
    # generate a list of dependency links for these package names
    # so setup can now understand them
    dependency_links = []
    return requirements, dependency_links


# get sourcecode version usually from git with some fallbacks
version = get_gitVersion()
print("version:", version)

# get dependencys and dependency install links to work with git urls
mutated_depends, mutated_links = get_requirements()
print("requirements:", mutated_depends)
print("requirement_links:", mutated_links)

# get
with open("README.md", "r") as fh:
    readme = fh.read()

# collect namespace packages but ignore certain undesired directories
packages = find_namespace_packages(
    exclude=("docs", "docs.*", "examples", "examples.*", "tests", "tests.*",
             "build", "build.*", "dist", "dist.*", "venv", "venv.*"))
print("namespace packages:", packages)

setup(
    name="nemesyst",
    version=version,
    description="Generalised, sequence-based, deep-learning framework of the" +
                "gods. Warning may include GANs, does not include nuts.",
    long_description=readme,
    long_description_content_type="text/markdown",
    author="George Onoufriou",
    url="https://github.com/DreamingRaven/nemesyst",
    packages=packages,
    scripts=['nemesyst'],
    # dependency_links=["git+https://github.com/DreamingRaven/python-ezdb.git#egg=python-ezdb-0.0.1"],
    dependency_links=mutated_links,
    install_requires=mutated_depends
)
