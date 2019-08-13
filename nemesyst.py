#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: nemesyst.py
# @Last modified by:   archer
# @Last modified time: 2019-08-13T11:42:27+01:00
# @License: Please see LICENSE file in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
# from six import reraise as raise_
from future.utils import raise_
import os
import sys

# argument handler
import getpass
import configargparse


def main(args):
    """Operate on processed args."""
    # mongodb handler
    from nemesyst_core.mongodb_handler import Mongo
    db = Mongo(args)  # matching args will override defaults
    if(args["db_init"] is True):
        db.init()  # creates database files
    if(args["db_start"] is True):
        db.start()  # launches database
    if(args["db_login"] is True):
        db.login()  # logs in to database
    if(args["db_stop"] is True):
        db.stop()  # stops database


main.__annotations__ = {"args": dict, "return": None}


def argument_parser(description=None, cfg_files=None):
    """Parse cli>environment>config>default arguments into dictionary."""
    home = os.path.expanduser("~")
    parser = configargparse.ArgumentParser(prog=None,
                                           description=description,
                                           add_help=False,
                                           default_config_files=cfg_files)
    nemesyst = parser.add_argument_group(title="Nemesyst options")
    data = parser.add_argument_group(title="Data pre-processing options")
    deeplearning = parser.add_argument_group(title="Deep learning options")
    mongodb = parser.add_argument_group(title="MongoDb options")

    # Nemesyst specific options
    nemesyst.add_argument("-h", "--help",
                          action="help",
                          help="Print help.")
    nemesyst.add_argument("-U", "--update",
                          default=bool(False),
                          action="store_true",
                          help="Nemesyst update, and restart.")
    nemesyst.add_argument("--prevent-update",
                          default=bool(False),
                          action="store_true",
                          help="Prevent nemesyst from updating.")
    nemesyst.add_argument("-c", "--config",
                          default=list(),
                          nargs='+',
                          type=type_file_path_exists,
                          help="List of all ini files to be used.")

    # data pre-processing specific options
    data.add_argument("-d", "--data",
                      default=list(),
                      nargs='+',
                      type=type_file_path_exists,
                      help="List of data file paths.")
    data.add_argument("--data-clean",
                      default=bool(False),
                      action="store_true",
                      help="Clean specified data files.")
    data.add_argument("--data-cleaner",
                      default=list(),
                      nargs='+',
                      type=type_file_path_exists,
                      help="Path to data cleaner(s).")
    data.add_argument("--data-import",
                      default=bool(False),
                      action="store_true",
                      help="Import (cleaned?) data to database.")

    # deep learning options
    deeplearning.add_argument("--dl-batch-size",
                              default=32,
                              type=int,
                              help="Batch size of the data to use.")

    # MongoDB specific options
    mongodb.add_argument("-l", "--db-login",
                         default=bool(False),
                         action="store_true",
                         help="Nemesyst log into mongodb.")
    mongodb.add_argument("-s", "--db-start",
                         default=bool(False),
                         action="store_true",
                         help="Nemesyst launch mongodb.")
    mongodb.add_argument("-S", "--db-stop",
                         default=bool(False),
                         action="store_true",
                         help="Nemesyst stop mongodb.")
    mongodb.add_argument("-i", "--db-init",
                         default=bool(False),
                         action="store_true",
                         help="Nemesyst initialise mongodb files.")
    mongodb.add_argument("--db-user-name",
                         type=str,
                         help="Set mongodb username.")
    mongodb.add_argument("--db-password",
                         default=bool(False),
                         action="store_true",
                         help="Set mongodb password.")
    mongodb.add_argument("--db-authentication",
                         default=str("SCRAM-SHA-1"),
                         type=str,
                         help="Set the mongodb authentication method.")
    mongodb.add_argument("--db-user-role",
                         default=str("readWrite"),
                         type=str,
                         help="Set the users permissions in the database.")
    mongodb.add_argument("--db-ip",
                         default=str("localhost"),
                         type=str,
                         help="The ip of the database to connect to.")
    mongodb.add_argument("--db-bind-ip",
                         default=str("localhost"),
                         type=str,
                         help="The ip the database should be accessible from.")
    mongodb.add_argument("--db-port",
                         default=str("65535"),
                         type=str,
                         help="The port both the unauth and auth db will use.")
    mongodb.add_argument("--db-name",
                         default=str("nemesyst"),
                         type=str,
                         help="The name of the authenticated database.")
    mongodb.add_argument("--db-collection-name",
                         default=str("test"),
                         type=str,
                         help="The name of the collection to use in database.")
    mongodb.add_argument("--db-path",
                         default=os.path.join(home, "/db"),
                         type=type_path,
                         help="The parent directory to use for the database.")
    mongodb.add_argument("--db-log-path",
                         default=os.path.join(home, "/db/log"),
                         type=type_path,
                         help="The parent directory to use for the db log.")
    mongodb.add_argument("--db-log-name",
                         default=str("mongo_log"),
                         type=str,
                         help="The base name of the log file to maintain.")
    mongodb.add_argument("--db-cursor-timeout",
                         default=600000,
                         type=int,
                         help="The duration in seconds before an unused " +
                              "cursor will time out.")
    mongodb.add_argument("--db-batch-size",
                         default=32,
                         type=int,
                         help="The number of documents to return from the " +
                              "db at once/ pre round.")
    mongodb.add_argument("--db-pipeline",
                         type=str,
                         help="The file path of the pipeline to use on db.")

    return parser


argument_parser.__annotations__ = {"description": str,
                                   "cfg_files": list,
                                   "return": any}


def type_path(string):
    """Create a path from string."""
    return os.path.abspath(string)


def type_file_path_exists(string):
    """Cross platform file path existance parser."""
    string = os.path.abspath(string)
    if os.path.isfile(string):
        return string
    else:
        # raise_(FileNotFoundError, str(string) + " does not exist.")
        raise_(ValueError, str(string) + " does not exist.")


type_path.__annotations__ = {"string": str, "return": str}


def argument_handler(args, config_files, description, isNewConfig=False):
    """Handle the argument parser."""
    parser = argument_parser(description=description,
                             cfg_files=config_files)
    processed_args = parser.parse_args(args)
    processed_args = vars(processed_args)
    if(processed_args["update"] is True) and \
            (processed_args["prevent_update"] is not True):
        # this will reboot this script
        new_args = [x for x in sys.argv if x != "-U"] + ["--prevent-update"]
        print("updating and restarting nemesyst at:", __file__)
        os.execv(__file__, new_args)
    if(processed_args["config"] is not None) and (isNewConfig is False):
        # this will reload this handler with a new config file
        processed_args = argument_handler(args,
                                          processed_args["config"] +
                                          config_files,
                                          description,
                                          isNewConfig=True)  # prevent loop
    if(processed_args["db_password"] is True):
        processed_args["db_password"] = getpass.getpass()
    return processed_args


argument_handler.__annotations__ = {"args": list,
                                    "description": str,
                                    "cfg_files": list,
                                    "return": any}


def import_cleaner():
    """Import cleaner(s) and call entry function."""
    pass


def import_learner():
    """Import learner script and call entry function."""
    pass


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
