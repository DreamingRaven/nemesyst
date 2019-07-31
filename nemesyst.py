#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2019-07-31
# @License: Please see LICENSE file in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import os
import sys

# argument handler
import getpass
import configargparse


def main(args):
    """Operate on processed args."""
    if(args["db_init"] is True):
        pass
    if(args["db_start"] is True):
        pass
    if(args["db_login"] is True):
        pass
    if(args["db_stop"] is True):
        pass


def argument_handler(args, config_files, description, isNewConfig=False):
    """Parse cli>environment>config>default arguments into dictionary."""
    cfg_files = config_files

    parser = configargparse.ArgumentParser(prog=None,
                                           description=description,
                                           add_help=False,
                                           default_config_files=cfg_files)
    nemesyst = parser.add_argument_group(title="Nemesyst options")
    mongodb = parser.add_argument_group(title="MongoDb options")
    passlib = parser.add_argument_group(title="Passlib options")

    # Nemesyst specific options
    nemesyst.add_argument("-h", "--help",
                          action="help",
                          help="print help")
    nemesyst.add_argument("-U", "--update",
                          default=bool(False),
                          action="store_true",
                          help="nemesyst update, and restart")
    nemesyst.add_argument("-c", "--config",
                          default=None,
                          help="nemesyst config path")

    # Passlib specific options
    passlib.add_argument("-P", "--passlib",
                         default=None,
                         help="passlib constructor dict")

    # MongoDB specific options
    mongodb.add_argument("-l", "--db-login",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst log into mongodb")
    mongodb.add_argument("-s", "--db-start",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst launch mongodb")
    mongodb.add_argument("-S", "--db-stop",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst stop mongodb")
    mongodb.add_argument("-i", "--db-init",
                         default=bool(False),
                         action="store_true",
                         help="nemesyst initialise mongodb")
    mongodb.add_argument("--db-user",
                         help="set mongodb usernam")
    mongodb.add_argument("--db-password",
                         default=bool(False),
                         action="store_true",
                         help="set mongodb password")

    processed_args = parser.parse_args(args)
    processed_args = vars(processed_args)

    if(processed_args["update"] is True):
        # this will reboot this script
        new_args = [x for x in sys.argv if x != "-U"]
        print("updating and restarting nemesyst at:", __file__)
        os.execv(__file__, new_args)
    if(processed_args["config"] is not None) and (isNewConfig is False):
        processed_args = argument_handler(args,
                                          [processed_args["config"]] +
                                          config_files,
                                          description,
                                          isNewConfig=True)  # prevent loop
    if(processed_args["db_password"] is True):
        processed_args["db_password"] = getpass.getpass()

    print(processed_args)
    return processed_args


if(__name__ == "__main__"):
    # passing the 3 needed args to argument handler and main with minimal
    # global footprint, so no assignment sorry
    main(argument_handler(
        # first arg, the set of cli args
        args=sys.argv[1:],
         # second arg, the list of default config locations
         config_files=[
            # https://unix.stackexchange.com/a/4047 .d extension
            "./nemesyst.d/*.conf",
            "/etc/nemesyst/nemesyst.d/*.conf",
        ],
        # the third arg, a description to be used in help
        description="Nemesyst; Hybrid-parallelisation database deep learning."
    ))
