#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2019-07-26
# @License: Please see LICENSE file in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import sys
import argparse


def main(args):
    pass


def argument_handler(args, description=None):
    default_description = "Nemesyst; Python hybrid parallelism deep learning"
    description = description if description is not None else \
        default_description

    parser = argparse.ArgumentParser(description=description)
    required = parser.add_argument_group(title="Required options")
    optional = parser.add_argument_group(title="Optional options")

    args = parser.parse_args(args)
    return args


if(__name__ == "__main__"):
    main(argument_handler(args=sys.argv[1:]))
