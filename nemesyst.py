#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2019-07-29
# @License: Please see LICENSE file in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import sys

# argument handler
import argparse
import getpass
import configparser


def main(args):
    pass


def argument_handler(args, description=None):
    """Parse cli and config arguments into dictionary"""
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
    nemesyst.add_argument("-l", "--login",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst log into mongodb")
    nemesyst.add_argument("-s", "--start-db",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst launch mongodb")
    nemesyst.add_argument("-s", "--stop-db",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst stop mongodb")
    nemesyst.add_argument("-i", "--init-db",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst initialise mongodb")

    # MongoDB specific options
    mongodb.add_argument("-u", "--user",
                         help="set mongodb usernam")
    mongodb.add_argument("-p", "--password",
                         type=str,
                         action=PasswordPromptAction,
                         help="set mongodb password")

    args = parser.parse_args(args)
    return vars(args)


class PasswordPromptAction(argparse.Action):
    """Argparse custom action for password input"""

    def __init__(self,
                 option_strings,
                 dest=None,
                 nargs=0,
                 default=None,
                 required=False,
                 type=None,
                 metavar=None,
                 help=None):
        super(PasswordPromptAction, self).__init__(
            option_strings=option_strings,
            dest=dest,
            nargs=nargs,
            default=default,
            required=required,
            metavar=metavar,
            type=type,
            help=help)

    def __call__(self, parser, args, values, option_string=None):
        """Getpass to get user password secureley."""
        password = getpass.getpass()
        setattr(args, self.dest, password)


if(__name__ == "__main__"):
    main(argument_handler(args=sys.argv[1:]))
