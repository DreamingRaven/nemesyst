#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2019-07-30
# @License: Please see LICENSE file in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import sys

# argument handler
import argparse
import getpass
import configparser


def main(args):
    if(args["init_db"] is True):
        pass
    if(args["start_db"] is True):
        pass
    if(args["login_db"] is True):
        pass
    if(args["stop_db"] is True):
        pass


def argument_handler(args, description=None):
    """Parse cli and config arguments into dictionary."""
    default_description = "Nemesyst; Python hybrid parallelism deep learning"
    description = description if description is not None else \
        default_description

    parser = argparse.ArgumentParser(prog=None,
                                     description=description,
                                     add_help=False)
    nemesyst = parser.add_argument_group(title="Nemesyst options")
    mongodb = parser.add_argument_group(title="MongoDb options")

    # Nemesyst specific options
    nemesyst.add_argument("-h", "--help",
                          action="help",
                          help="print help")
    nemesyst.add_argument("-U", "--update",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst update, and restarta")

    # MongoDB specific options
    mongodb.add_argument("-l", "--login-db",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst log into mongodb")
    mongodb.add_argument("-s", "--start-db",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst launch mongodb")
    mongodb.add_argument("-S", "--stop-db",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst stop mongodb")
    mongodb.add_argument("-i", "--init-db",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst initialise mongodb")
    mongodb.add_argument("-u", "--user",
                         help="set mongodb usernam")
    mongodb.add_argument("-p", "--password",
                         default=None,
                         action="store_true",
                         help="set mongodb password")

    args = parser.parse_args(args)
    args = vars(args)

    if(args["password"] is True):
        args["password"] = getpass.getpass()

    print(args)
    return args


if(__name__ == "__main__"):
    main(argument_handler(args=sys.argv[1:]))
