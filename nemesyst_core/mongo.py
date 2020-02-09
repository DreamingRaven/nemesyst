#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2019-07-15
# @Email:  george raven community at pm dot me
# @Filename: mongo_handler.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import os
import subprocess
import time
from pymongo import MongoClient, errors, database, command_cursor
import gridfs
import re


class Mongo(object):
    """Python2/3 compatible MongoDb utility wrapper.

    This wrapper saves its state in an internal overridable dictionary
    such that you can adapt it to your requirements, if you should need to do
    something unique, the caveat being it becomes harder to read.

    :param args: Dictionary of overides.
    :param logger: Function address to print/ log to (default: print).
    :type args: dictionary
    :type logger: function address
    :example: Mongo({"db_user_name": "someUsername",
                     "db_password": "somePassword"})
    :example: Mongo()
    """

    def __init__(self, args=None, logger=None):
        """Init class with defaults.

        optionally accepts dictionary of default overides.
        """
        args = args if args is not None else dict()
        self.home = os.path.expanduser("~")
        defaults = {
            # generic options section
            "db_user_name": "groot",
            "db_password": "iamgroot",
            "db_config_path": None,
            "db_intervention": False,
            "db_authentication": "SCRAM-SHA-1",
            "db_authentication_database": None,
            "db_user_role": "readWrite",
            "db_ip": "localhost",
            "db_bind_ip": ["localhost"],
            "db_name": "nemesyst",
            "db_collection_name": "test",
            "db_port": "27017",
            "db_path": "db",
            "db_log_path": "db" + "/log",
            "db_log_name": "mongoLog",
            "db_cursor_timeout": 600000,
            "db_batch_size": 32,
            "pylog": logger if logger is not None else print,
            "db": None,
            "db_pipeline": None,
            "gfs": None,
            # replica options section
            "db_replica_set_name": None,
            "db_replica_read_preference": "primary",
            "db_replica_max_staleness": -1,
            # tls options section
            "db_tls": False,
            "db_tls_ca_file": None,
            "db_tls_certificate_key_file": None,
            "db_tls_certificate_key_file_password": None,
            "db_tls_crl_file": None,

        }
        self.args = self._mergeDicts(defaults, args)
        # final adjustments to newly defined dictionary
        self.args["db_path"] = os.path.abspath(self.args["db_path"])
        self.args["db_log_path"] = os.path.abspath(self.args["db_log_path"])

    __init__.__annotations__ = {"args": dict, "logger": print, "return": None}

    def init(self, db_path=None, db_log_path=None, db_log_name=None,
             db_config_path=None):
        """Initialise the database.

        Includes ensuring db path and db log path exist and generating,
        creating the DB files, and adding an authentication user.
        All of this should be done on a localhost port so that the
        unprotected database is never exposed.

        :param db_path: Desired directory of MongoDB database files.
        :param db_log_path: Desired directory of MongoDB log files.
        :param db_log_name: Desired name of log file.
        :param db_config_path: Config file to pass to MongoDB.
        :type db_path: string
        :type db_config_path: string
        :type db_log_path: string
        :type db_log_name: string
        """
        db_path = db_path if db_path is not None else self.args["db_path"]
        db_log_path = db_log_path if db_log_path is not None else \
            self.args["db_log_path"]
        db_log_name = db_log_name if db_log_name is not None else \
            self.args["db_log_name"]
        db_config_path = db_config_path if db_config_path is not None else \
            self.args["db_config_path"]

        self.stop()

        time.sleep(2)

        # create directories
        subprocess.call([
            "mkdir", "-p",
            str(db_path),
            str(db_log_path),
        ])
        cli_args = [  # non authentication version of db start
            "mongod",
            "--bind_ip",        "localhost",
            "--port",           self.args["db_port"],
            "--dbpath",         str(db_path),
            "--logpath",        str(os.path.join(db_log_path, db_log_name)),
            "--quiet"
        ]

        if(db_config_path is not None):
            pass
            cli_args += [
                "--config", str(db_config_path)
            ]

        self.args["pylog"]("Launching unauth db on localhost", cli_args)
        # launch unauth db
        subprocess.Popen(cli_args)
        # wait for db to come up
        time.sleep(2)
        # connect to db in local scope
        self._addUser()
        # manual intervention if desired
        if(self.args["db_intervention"]):
            # INITIATING MANUAL SUPERPOWERS
            self.login(db_ip="localhost")
        # close the unauth db
        self.stop()

    init.__annotations__ = {"db_path": str, "db_log_path": str,
                            "db_log_name": str, "db_config_path": str,
                            "return": None}

    def connect(self, db_ip=None, db_port=None, db_authentication=None,
                db_authentication_database=None,
                db_user_name=None, db_password=None, db_name=None,
                db_replica_set_name=None, db_replica_read_preference=None,
                db_replica_max_staleness=None, db_tls=None,
                db_tls_ca_file=None, db_tls_certificate_key_file=None,
                db_tls_certificate_key_file_password=None,
                db_tls_crl_file=None,
                db_collection_name=None):
        """Connect to a specific mongodb database.

        This sets the internal db client which is neccessary to connect to
        and use the associated database. Without it operations such as dump
        into the database will fail. This is replica set capable.

        :param db_ip: Database hostname or ip to connect to.
        :param db_port: Database port to connect to.
        :param db_authentication: The authentication method to use on db.
        :param db_user_name: Username to use for authentication to db_name.
        :param db_password: Password for db_user_name in database db_name.
        :param db_name: The name of the database to connect to.
        :param db_replica_set_name: Name of the replica set to connect to.
        :param db_replica_read_preference: What rep type to prefer reads from.
        :param db_replica_max_staleness: Max seconds behind is replica allowed.
        :param db_tls: use TLS for db connection.
        :param db_tls_certificate_key_file: Certificate and key file for tls.
        :param db_tls_certificate_key_file_password: Cert and key file pass.
        :param db_tls_crl_file: Certificate revocation list file path.
        :param db_collection_name: GridFS collection to use.
        :type db_ip: string
        :type db_port: string
        :type db_authentication: string
        :type db_user_name: string
        :type db_password: string
        :type db_name: string
        :type db_replica_set_name: string
        :type db_replica_read_preference: string
        :type db_replica_max_staleness: string
        :type db_tls: bool
        :type db_tls_certificate_key_file: string
        :type db_tls_certificate_key_file_password: string
        :type db_tls_crl_file: string
        :type db_collection_name: string
        :return: database client object
        :rtype: pymongo.database.Database
        """

        # ip
        db_ip = db_ip if db_ip is not None else self.args["db_ip"]
        # port
        db_port = db_port if db_port is not None else self.args["db_port"]
        # authentication mechanism name
        db_authentication = db_authentication if db_authentication is not \
            None else self.args["db_authentication"]
        # authentication destination db name
        db_authentication_database = db_authentication_database if\
            db_authentication_database is not \
            None else self.args["db_authentication_database"]
        # username
        db_user_name = db_user_name if db_user_name is not None else \
            self.args["db_user_name"]
        # password
        db_password = db_password if db_password is not None else \
            self.args["db_password"]
        # database name
        db_name = db_name if db_name is not None else self.args["db_name"]
        # replica set name
        db_replica_set_name = db_replica_set_name if db_replica_set_name is \
            not None else self.args["db_replica_set_name"]
        # replica read preference
        db_replica_read_preference = db_replica_read_preference if \
            db_replica_read_preference is not None else \
            self.args["db_replica_read_preference"]
        # replica staleness
        db_replica_max_staleness = db_replica_max_staleness if \
            db_replica_max_staleness is not None else \
            self.args["db_replica_max_staleness"]
        # to use tls?
        db_tls = db_tls if db_tls is not None else self.args["db_tls"]
        # certificate authoritys certificate file
        db_tls_ca_file = db_tls_ca_file if db_tls_ca_file is not None else \
            self.args["db_tls_ca_file"]
        # client certificate & key file
        db_tls_certificate_key_file = db_tls_certificate_key_file if \
            db_tls_certificate_key_file is not None else \
            self.args["db_tls_certificate_key_file"]
        # client certificate and key file password
        db_tls_certificate_key_file_password = \
            db_tls_certificate_key_file_password if \
            db_tls_certificate_key_file_password is not None else \
            self.args["db_tls_certificate_key_file_password"]
        # tls revocation certificates file
        db_tls_crl_file = db_tls_crl_file if db_tls_crl_file is not None else \
            self.args["db_tls_crl_file"]
        # collection name
        db_collection_name = db_collection_name if db_collection_name is not \
            None else self.args["db_collection_name"]

        client_args = {}
        client_args["host"] = ["{0}:{1}".format(str(db_ip), str(db_port))]

        if (db_authentication is not None) and (db_authentication != ""):
            # authentication
            client_args["authMechanism"] = db_authentication
            client_args["username"] = db_user_name
            client_args["password"] = db_password
            client_args["authSource"] = db_authentication_database if \
                db_authentication_database is not None else db_name

        if (db_replica_set_name is not None):
            # replica set
            client_args["replicaset"] = db_replica_set_name
            client_args["readPreference"] = db_replica_read_preference
            client_args["maxStalenessSeconds"] = db_replica_max_staleness

        if (db_tls is not None):
            # tls
            client_args["tls"] = db_tls  # False
            client_args["tlsCAFile"] = db_tls_ca_file  # None
            client_args["tlsCertificateKeyFile"] = db_tls_certificate_key_file
            client_args["tlsCertificateKeyFilePassword"] =  \
                db_tls_certificate_key_file_password  # None
            client_args["tlsCRLFile"] = db_tls_crl_file  # None
        # TODO add these in next if user has them seperate
        # client_args["ssl_certfile"] = None
        # client_args["ssl_keyfile"] = None

        client = MongoClient(**client_args)

        db = client[db_name]
        self.args["db"] = db
        return db

    connect.__annotations__ = {"db_ip": str,
                               "db_port": str,
                               "db_authentication": str,
                               "db_user_name": str,
                               "db_password": str,
                               "db_name": str,
                               "db_replica_set_name": str,
                               "db_collection_name": str,
                               "db_replica_read_preference": str,
                               "db_replica_max_staleness": str,
                               "db_tls": bool,
                               "db_tls_ca_file": str,
                               "db_tls_certificate_key_file": str,
                               "db_tls_certificate_key_file_password": str,
                               "db_tls_crl_file": str,
                               "return": database.Database}

    def login(self, db_port=None, db_user_name=None, db_password=None,
              db_name=None, db_ip=None):
        """Log in to database, interrupt, and availiable via cli.

        :param db_port: Database port to connect to.
        :param db_user_name: Database user to authenticate as.
        :param db_password: User password to authenticate with.
        :param db_name: Database to authenticate to, the authentication db.
        :param db_ip: Database ip to connect to.
        :type db_port: string
        :type db_user_name: string
        :type db_password: string
        :type db_name: string
        :type db_ip: string
        """
        db_port = db_port if db_port is not None else self.args["db_port"]
        db_user_name = db_user_name if db_user_name is not None else \
            self.args["db_user_name"]
        db_password = db_password if db_password is not None else \
            self.args["db_password"]
        db_name = db_name if db_name is not None else self.args["db_name"]
        db_ip = db_ip if db_ip is not None else self.args["db_ip"]

        loginArgs = [
            "mongo",
            "--port", str(db_port),
            "-u",   str(db_user_name),
            "-p", str(db_password),
            "--authenticationDatabase", str(db_name),
            str(db_ip)
        ]
        subprocess.call(loginArgs)

    login.__annotations__ = {"db_port": str, "db_user_name": str,
                             "db_password": str, "db_name": str, "db_ip": str,
                             "return": None}

    def start(self, db_ip=None, db_port=None, db_path=None, db_log_path=None,
              db_log_name=None, db_cursor_timeout=None, db_config_path=None,
              db_replica_set_name=None):
        """Launch an on machine database with authentication.

        :param db_ip: List of IPs to accept connectiongs from.
        :param db_port: Port desired for database.
        :param db_path: Path to parent dir of database.
        :param db_log_path: Path to parent dir of log files.
        :param db_log_name: Desired base name for log files.
        :param db_cursor_timeout: Set timeout time for unused cursors.
        :param db_path: Config file path to pass to MongoDB.
        :type db_ip: list
        :type db_port: string
        :type db_path: string
        :type db_log_path: string
        :type db_log_name: string
        :type db_cursor_timeout: integer
        :type db_config_path: string
        :rtype: subprocess.Popen
        :return: Subprocess of running MongoDB.
        """
        db_bind_ip = db_ip if db_ip is not None else self.args["db_bind_ip"]
        db_port = db_port if db_port is not None else self.args["db_port"]
        db_path = db_path if db_path is not None else self.args["db_path"]
        db_log_path = db_log_path if db_log_path is not None else \
            self.args["db_log_path"]
        db_log_name = db_log_name if db_log_name is not None else \
            self.args["db_log_name"]
        db_cursor_timeout = db_cursor_timeout if db_cursor_timeout is not \
            None else self.args["db_cursor_timeout"]
        db_replica_set_name = db_replica_set_name if db_replica_set_name is \
            not None else self.args["db_replica_set_name"]

        self.args["pylog"]("Starting mongodb: auth=",
                           str(self.args["db_authentication"]))
        cli_args = [
            "mongod",
            "--bind_ip",        ','.join(map(str, db_bind_ip)),
            "--port",           str(db_port),
            "--dbpath",         str(db_path),
            "--logpath",        str(os.path.join(db_log_path, db_log_name)),
            "--setParameter",   str("cursorTimeoutMillis=" +
                                    str(db_cursor_timeout)),
            "--auth",
            "--quiet"
        ]

        if(db_replica_set_name is not None):
            cli_args += [
                "--replSet", str(db_replica_set_name)
            ]
        if(db_config_path is not None):
            pass
            cli_args += [
                "--config", str(db_config_path)
            ]
        time.sleep(2)
        db_process = subprocess.Popen(cli_args)
        time.sleep(2)
        self.args["db_process"] = db_process
        return db_process

    start.__annotations__ = {"db_ip": str, "db_bind_ip": list,
                             "db_port": str, "db_path": str,
                             "db_log_path": str, "db_log_name": str,
                             "db_cursor_timeout": int,
                             "db_replica_set_name": str,
                             "db_config_path": str,
                             "return": subprocess.Popen}

    def stop(self, db_path=None):
        """Stop a running local database.

        :param db_path: The path to the database to shut down.
        :type db_path: string
        :return: Subprocess of database closer.
        :rtype: subprocess.Popen
        """
        db_path = db_path if db_path is not None else self.args["db_path"]

        self.args["pylog"]("Shutting down MongoDB.")
        process = subprocess.Popen(
            ["mongod",
             "--dbpath", str(db_path),
             "--shutdown"]
        )
        time.sleep(0.5)
        return process

    stop.__annotations__ = {"return": subprocess.Popen}

    def _addUser(self):
        """Add a user with given permissions to the authentication database."""
        local_mongourl = "mongodb://{0}:{1}/".format(
            "localhost", self.args["db_port"])
        # self.args["pylog"]("Adding  mongodb user:",
        #                    str(self.args["db_user_name"]),
        #                    ", pass:",
        #                    str(type(self.args["db_password"])),
        #                    ", role:", str(self.args["db_user_role"]),
        #                    ", authdb:", str(self.args["db_name"]))
        debug_status = {
            "mongodb-user:": self.args["db_user_name"],
            "user-password": type(self.args["db_password"]),
            "role": self.args["db_user_role"],
            "authdb": self.args["db_name"],
            "mongo-url": local_mongourl
        }
        self.args["pylog"]("Adding user:", debug_status)
        client = MongoClient(local_mongourl)
        db = client[self.args["db_name"]]
        try:
            if(self.args["db_user_role"] == "all"):
                db.command("createUser",
                           self.args["db_user_name"],
                           pwd=self.args["db_password"],
                           roles=["readWrite", "dbAdmin"])
            else:
                db.command("createUser",
                           self.args["db_user_name"],
                           pwd=self.args["db_password"],
                           roles=[self.args["db_user_role"]])
        except errors.DuplicateKeyError:  # it used to be a duplicate key error
            self.args["pylog"](self.args["db_user_name"] + "@" +
                               self.args["db_name"],
                               "already exists skipping (DuplicateKeyError).")
        except errors.OperationFailure as e:
            # in a new version of pymongo if a user exists already it is now
            # no longer a duplicate key error, so we have to split a genuine
            # operation failure vs an already existing user which is fine.
            # pacman -Q python-pymongo = 3.9.0-1 so this version breaks it
            self.args["pylog"]("can not add user:",
                               str(self.args["db_user_name"]) + "@" +
                               str(self.args["db_name"]),
                               "ensure correct " +
                               "--db-user-name, and " +
                               "--db-password are being used.")
            split_e = re.split('\W+', str(e))
            if(split_e[-2] == "already") and (split_e[-1] == "exists"):
                self.args["pylog"]("user already exists, skipping.")
            else:
                raise

    _addUser.__annotations__ = {"return": None}

    def debug(self):
        """Log function to help track the internal state of the class.

        Simply logs working state of args dict.
        """
        self.args["pylog"](self.args)

    debug.__annotations__ = {"return": None}

    def dump(self, db_collection_name, data, db=None):
        """Import data dictionary into database.

        :param db_collection_name: Collection name to import into.
        :param data: Data to import into database.
        :param db: Database to import data into.
        :type db_collection_name: string
        :type data: dictionary
        :type db: pymongo.database.Database
        :example: dump(db_collection_name="test",
                       data={"subdict":{"hello": "world"}})
        """
        db = db if db is not None else self.args["db"]

        if isinstance(data, dict) and data:
            db[str(db_collection_name)].insert_one(data)
        elif isinstance(data, tuple) and data:
            gfs = gridfs.GridFS(db, collection=db_collection_name)
            gfs.put(data[1], **data[0])

    dump.__annotations__ = {"db_collection_name": str, "data": dict,
                            "db": database.Database, "return": None}

    def _mergeDicts(self, *dicts):
        """Given multiple dictionaries, merge together in order."""
        result = {}
        for dictionary in dicts:
            result.update(dictionary)  # merge each dictionary in order
        return result

    _mergeDicts.__annotations__ = {"dicts": dict, "return": dict}

    def getCursor(self, db=None, db_pipeline=None, db_collection_name=None):
        """Use aggregate pipeline to get a data-cursor from the database.

        This cursor is what mongodb provides to allow you to request the data
        from the database in a manner you control, instead of just getting
        a big dump from the database.

        :param db_pipeline: Mongodb aggregate pipeline data to transform and
            retrieve the data as you request.
        :param db_collection_name: The collection name which we will pull data
            from using the aggregate pipeline.
        :param db: Database object to operate pipeline on.
        :type db_pipeline: list of dicts
        :type db_collection_name: str
        :type db: pymongo.database.Database
        :return: Command cursor to fetch the data with.
        :rtype: pymongo.command_cursor.CommandCursor
        """
        db_pipeline = db_pipeline if db_pipeline is not None else \
            self.args["db_pipeline"]
        db_collection_name = db_collection_name if db_collection_name is not \
            None else self.args["db_collection_name"]
        db = db if db is not None else self.args["db"]
        # from string to pymongo.collection.Collection
        db_collection = db[db_collection_name]
        db_data_cursor = db_collection.aggregate(db_pipeline,
                                                 allowDiskUse=True)
        self.args["db_data_cursor"] = db_data_cursor
        return db_data_cursor

    getCursor.__annotations__ = {"db_pipeline": list,
                                 "db_collection_name": str,
                                 "db": database.Database,
                                 "return": command_cursor.CommandCursor}

    def getBatches(self, db_batch_size=None, db_data_cursor=None):
        """Get database cursor data in batches.

        :param db_batch_size: The number of items to return in a single round.
        :param db_data_cursor: The cursor to use to retrieve data from db.
        :type db_batch_size: integer
        :type db_data_cursor: command_cursor.CommandCursor
        :return: yields a list of items requested.
        :rtype: list of dicts
        :todo: desperateley needs a rewrite and correction of bug. Last value
            always fails. I want this in a magic function too to make it easy.
        """
        db_batch_size = db_batch_size if db_batch_size is not None else \
            self.args["db_batch_size"]
        db_data_cursor = db_data_cursor if db_data_cursor is not None else \
            self.args["db_data_cursor"]

        cursor = db_data_cursor
        if(cursor is not None):
            while(cursor.alive):
                yield self._nextBatch(cursor, db_batch_size)
            self.args["pylog"]("cursor is now dead.")
        else:
            self.args["pylog"]("Your cursor is None, please Mongo.connect()")

    getBatches.__annotations__ = {"db_batch_size": int,
                                  "db_data_cursor":
                                  command_cursor.CommandCursor,
                                  "return": list}

    def getFiles(self, db_batch_size=None, db_data_cursor=None,
                 db_collection_name=None, db=None):
        """Get gridfs files from mongodb by id using cursor to .files.

        :param db_batch_size: The number of items to return in a single round.
        :param db_data_cursor: The cursor to use to retrieve data from db.
        :param db_collection_name: The top level collecton name
            not including .chunks or .files where gridfs is to operate.
        :param db: Database object to operate pipeline on.
        :type db_batch_size: integer
        :type db_data_cursor: command_cursor.CommandCursor
        :type db_collection_name: str
        :type db: pymongo.database.Database
        :return: yields a list of tuples containing (item requested, metadata).
        """
        db_data_cursor = db_data_cursor if db_data_cursor is not None else \
            self.args["db_data_cursor"]
        db_batch_size = db_batch_size if db_batch_size is not None else \
            self.args["db_batch_size"]
        db_collection_name = db_collection_name if db_collection_name is not \
            None else self.args["db_collection_name"]
        db = db if db is not None else self.args["db"]

        gfs = gridfs.GridFS(db, collection=db_collection_name)
        for batch in self.getBatches(db_batch_size=db_batch_size,
                                     db_data_cursor=db_data_cursor):
            gridout_list = list(map(
                lambda doc: {"gridout": gfs.get(doc["_id"]),
                             "_id": doc["_id"]}, batch))
            # # equivalent for loop
            # gridout_list = []
            # for doc in batch:
            #     gridout_list.extend({"gridout": gfs.get(doc["_id"]),
            #                          "_id": doc["_id"]})
            yield gridout_list

    getFiles.__annotations__ = {"db_batch_size": int,
                                "db_data_cursor": command_cursor.CommandCursor,
                                "db_collection_name": str,
                                "db": database.Database,
                                "return": list}

    def _nextBatch(self, cursor, db_batch_size):
        """Return the very next batch in mongoDb cursor."""
        batch = []
        try:
            while(len(batch) < db_batch_size):
                # cursor.batch_size(0) # batch size not yet set
                singleExample = cursor.next()
                batch.append(singleExample)
        except StopIteration:
            pass  # will eventually reach the end
        return batch

    def __setitem__(self, key, value):
        """Set a single arg or state by, (key, value)."""
        self.args[key] = value

    __setitem__.__annotations__ = {"key": str, "value": any, "return": None}

    def __getitem__(self, key):
        """Get a single arg or state by, (key, value)."""
        try:
            return self.args[key]
        except KeyError:
            return None  # does not exist is the same as None, gracefull catch

    __getitem__.__annotations__ = {"key": str, "return": any}

    def __delitem__(self, key):
        """Delete a single arg or state by, (key, value)."""
        try:
            del self.args[key]
        except KeyError:
            pass  # job is not done but equivalent outcomes so will not error

    __delitem__.__annotations__ = {"key": str, "return": None}

    def __iter__(self):
        """Iterate through housed dictionary, for looping."""
        raise NotImplementedError("iter() is not yet implemented")
        # self.db.connect()
        # cursor = self.db.getData(pipeline=self.getPipe(
        #     self.args["pipeline"]), db_collection_name=self.args["coll"])
        #
        # while(cursor.alive):
        #     try:
        #         yield self._nextBatch(cursor)
        #     except StopIteration:
        #         return

    __iter__.__annotations__ = {"return": any}

    def __len__(self):
        """Return the first order length of the dictionary."""
        return len(self.args)

    __len__.__annotations__ = {"return": int}


def _mongo_unit_test():
    """Unit test of MongoDB compat."""
    import datetime
    import pickle
    # create Mongo object to use
    db = Mongo({"test2": 2, "db_port": "65535"})
    # testing magic functions
    db["test2"] = 3  # set item
    db["test2"]  # get item
    len(db)  # len
    del db["test2"]  # del item
    # output current state of Mongo
    db.debug()
    # stop any active databases already running at the db path location
    db.stop()
    # hold for 2 seconds to give the db time to start
    time.sleep(2)
    # attempt to initialise the database, as in create the database with users
    db.init()
    # hold to let the db to launch the now new unauthenticated db
    time.sleep(2)
    # start the authenticated db, you will now need a username password access
    db.start()
    # warm up time for new authentication db
    time.sleep(2)
    # create a connection to the database so we can do database operations
    db.connect()
    db.debug()
    # import data into mongodb debug collection
    db.dump(db_collection_name="test", data={
        "string": "99",
        "number": 99,
        "binary": bin(99),
        "subdict": {"hello": "world"},
        "subarray": [{"hello": "worlds"}, {"hi": "jim"}],
        "timedate": datetime.datetime.utcnow(),
    })
    # testing gridfs insert item into database
    db.dump(db_collection_name="test", data=(
        {"utctime": datetime.datetime.utcnow()},
        pickle.dumps("some_test_string")
    ))
    # log into the database so user can manually check data import
    db.login()
    # attempt to retrieve the data that exists in the collection as a cursor
    c = db.getCursor(db_collection_name="test", db_pipeline=[{"$match": {}}])
    # itetate through the data in batches to minimise requests
    for dataBatch in db.getBatches(db_batch_size=32, db_data_cursor=c):
        print("Returned number of documents:", len(dataBatch))
    # define a pipeline to get the latest gridfs file in a given collection
    fs_pipeline = [{'$sort': {'uploadDate': -1}},
                   {'$limit': 5},
                   {'$project': {'_id': 1}}]
    # get a cursor to get us the ID of files we desire
    fc = db.getCursor(db_collection_name="test.files", db_pipeline=fs_pipeline)
    # use cursor and get files to collect our data in batches
    for batch in db.getFiles(db_batch_size=2, db_data_cursor=fc):
        print(batch)
    # finally close out database
    db.stop()


if(__name__ == "__main__"):
    _mongo_unit_test()
