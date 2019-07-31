# @Author: George Onoufriou <archer>
# @Date:   2019-07-31
# @Email:  george raven community at pm dot me
# @Filename: conf.py
# @Last modified by:   archer
# @Last modified time: 2019-08-01
# @License: Please see LICENSE in project root


# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))
import sphinx_rtd_theme
import subprocess


# -- Project information -----------------------------------------------------

project = 'Nemesyst'
copyright = '2017, George Onoufriou (GeorgeRaven, archer)'
author = 'GeorgeRaven'
master_doc = 'index'

# The full version, including alpha/beta/rc tags
# autogenerating version number in Archlinux style
# git describe --long | sed 's/\([^-]*-\)g/r\1/;s/-/./g
git_describe = subprocess.Popen(["git", "describe", "--long"],
                                stdout=subprocess.PIPE)
version_num = subprocess.check_output(["sed", r"s/\([^-]*-\)g/r\1/;s/-/./g"],
                                      stdin=git_describe.stdout)
git_describe.wait()
version_num = version_num.decode("ascii").strip()
print(project, "version:", version_num)
release = version_num


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_rtd_theme"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"  # 'alabaster'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []  # ['_static']
