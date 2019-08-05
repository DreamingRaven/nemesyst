# @Author: George Onoufriou <archer>
# @Date:   2019-07-15
# @Email:  george raven community at pm dot me
# @Filename: mongo_compat.py
# @Last modified by:   archer
# @Last modified time: 2019-08-05
# @License: Please see LICENSE in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import os
import subprocess
import time
from pymongo import MongoClient, errors, database


class Mongo(object):
    """Python2/3 compatible MongoDb utility wrapper.

    This wrapper saves its state in an internal overridable dictionary
    such that you can adapt it to your requirements, if you should need to do
    something unique, the caveat being it becomes harder to read.

    :param args: dictionary of overides
    :param logger: function address to print/ log to (default: print)
    :type args: dictionary
    :type logger: function address
    :example: Mongo({"db_user": "someUsername",
                     "db_pass": "somePassword"})
    :example: Mongo()
    """

    def __init__(self, args=None, logger=None):
        """Init class with defaults.

        optionally accepts dictionary of default overides.
        """
        args = args if args is not None else dict()
        self.home = os.path.expanduser("~")
        defaults = {
            "db_user": "groot",
            "db_pass": "iamgroot",
            "db_authentication": "SCRAM-SHA-1",
            "db_user_role": "readWrite",
            "db_ip": "127.0.0.1",
            "db_name": "RecSyst",
            "db_collection_name": "testColl",
            "db_port": "27017",
            # "db_url": "mongodb://localhost:27017/", # this is auto generated
            "db_path": self.home + "/db",
            "db_log_path": self.home + "/db" + "/log",
            "db_log_name": "mongoLog",
            "db_cursor_timeout": 600000,
            "db_batch_size": 32,
            "pylog": logger if logger is not None else print,
            "db_ssl": None,
            "db": None,
            "db_pipeline": None,
        }
        self.args = self._merge_dicts(defaults, args)
        # final adjustments to newly defined dictionary
        self.args["db_url"] = "mongodb://{0}:{1}/".format(
            self.args["db_ip"], self.args["db_port"])

    __init__.__annotations__ = {"args": dict, "logger": print, "return": None}

    def initDb(self):
        """Initialise the database.

        Includes ensuring db path and db log path exist and generating,
        creating the DB files, and adding an authentication user.
        All of this should be done on a localhost port so that the
        unprotected database is never exposed.
        """
        # create directories
        subprocess.call([
            "mkdir", "-p",
            str(self.args["db_path"]),
            str(self.args["db_log_path"]),
        ])
        cliArgs = [  # non authentication version of db start
            "mongod",
            "--bind_ip",        "127.0.0.1",
            "--port",           "27017",
            "--dbpath",         str(self.args["db_path"]),
            "--logpath",        str(self.args["db_log_path"] +
                                    self.args["db_log_name"]),
            "--quiet"
        ]
        self.args["pylog"]("Launching unauth db on localhost")
        # launch unauth db
        subprocess.Popen(cliArgs)
        # wait for db to come up
        time.sleep(2)
        # connect to db in local scope
        self._addUser()
        # close the unauth db
        self.stop()

    initDb.__annotations__ = {"return": None}

    def connect(self, db_url=None, db_user=None, db_pass=None, db_name=None,
                db_authentication=None):
        """Connect to a specific mongodb database.

        This sets the internal db client which is neccessary to connect to
        and use the associated database. Without it operations such as imports
        into the database will fail.

        :param db_url: database url (default: "mongodb://localhost:27017/")
        :param db_user: username to use for authentication to db_name
        :param db_pass: password for db_user in database db_name
        :param db_name: the name of the database to connect to
        :param db_authentication: the authentication method to use on db
        :type db_url: string
        :type db_user: string
        :type db_pass: string
        :type db_name: string
        :type db_authentication: string
        :return: database client object
        :rtype: pymongo.database.Database
        """
        db_url = db_url if db_url is not None else self.args["db_url"]
        db_user = db_user if db_user is not None else self.args["db_user"]
        db_pass = db_pass if db_pass is not None else self.args["db_pass"]
        db_name = db_name if db_name is not None else self.args["db_name"]
        db_authentication = db_authentication if db_authentication is not \
            None else self.args["db_authentication"]

        client = MongoClient(
            db_url,
            username=str(db_user),
            password=str(db_pass),
            authSource=str(db_name),
            authMechanism=str(db_authentication))
        db = client[db_name]
        self.args["db"] = db
        return db

    connect.__annotations__ = {"db_url": str, "db_user": str,
                               "db_pass": str, "db_name": str,
                               "db_authentication": str,
                               "return": database.Database}

    def login(self):
        """Log in to database, interupt, and availiable via cli."""
        loginArgs = [
            "mongo",
            "--port", str(self.args["db_port"]),
            "-u",   str(self.args["db_user"]),
            "-p", str(self.args["db_pass"]),
            "--authenticationDatabase", str(self.args["db_name"])
        ]
        subprocess.call(loginArgs)

    login.__annotations__ = {"return": None}

    def start(self):
        """Launch the database."""
        self.args["pylog"]("Starting mongodb: auth=",
                           str(self.args["db_authentication"]))
        cliArgs = [
            "mongod",
            "--bind_ip",        str(self.args["db_ip"]),
            "--port",           str(self.args["db_port"]),
            "--dbpath",         str(self.args["db_path"]),
            "--logpath",        str(self.args["db_log_path"] +
                                    self.args["db_log_name"]),
            "--setParameter",   str("cursorTimeoutMillis=" +
                                    str(self.args["db_cursor_timeout"])),
            "--auth",
            "--quiet"
        ]
        self.args["mongoProcess"] = subprocess.Popen(cliArgs)

    start.__annotations__ = {"return": None}

    def stop(self):
        """Stop a running local database."""
        self.args["pylog"]("Shutting down MongoDB.")
        subprocess.Popen(
            ["mongod",
             "--dbpath", str(self.args["db_path"]),
             "--shutdown"]
        )

    stop.__annotations__ = {"return": None}

    def _addUser(self):
        """Add a user with given permissions to the authentication database."""
        self.args["pylog"]("Adding  mongodb user:",
                           str(self.args["db_user"]),
                           ", role:", str(self.args["db_user_role"]),
                           ", authdb:", str(self.args["db_name"]))
        client = MongoClient("mongodb://localhost:27017/")
        db = client[self.args["db_name"]]
        try:
            if(self.args["db_user_role"] == "all"):
                db.command("createUser",
                           self.args["db_user"],
                           pwd=self.args["db_pass"],
                           roles=["readWrite", "dbAdmin"])
            else:
                db.command("createUser",
                           self.args["db_user"],
                           pwd=self.args["db_pass"],
                           roles=[self.args["db_user_role"]])
        except errors.DuplicateKeyError:
            self.args["pylog"](self.args["db_user"] + "@" +
                               self.args["db_name"],
                               "already exists skipping.")
    _addUser.__annotations__ = {"return": None}

    def debug(self):
        """Log function to help track the internal state of the class."""
        self.args["pylog"](self.args)

    debug.__annotations__ = {"return": None}

    def imports(self, collection, json=None, dictionary=None):
        """Import data of specified format into MongoDB.

        Takes a collection name and one of either json or dictionary and
        imports it to the specified collection.
        """
        if(json is not None):
            raise NotImplementedError("direct json import is not yet ready")
            # data = json_util.loads(json)
        elif (dictionary is not None):
            self.args["db"][str(collection)].insert_one(dictionary)

    imports.__annotations__ = {"return": None}

    def _merge_dicts(self, *dicts):
        """Given multiple dictionaries, merge together in order."""
        result = {}
        for dictionary in dicts:
            result.update(dictionary)  # merge each dictionary in order
        return result

    _merge_dicts.__annotations__ = {"dicts": dict, "return": None}

    def getCursor(self, pipeline=None, collection=None):
        """Get data from database using provided aggregate pipeline.

        Returns data as dictionary.
        """
        pipeline = pipeline if pipeline is not None else \
            self.args["db_pipeline"]
        collection = collection if collection is not None else \
            self.args["collName"]  # set collection name wanted
        collection = self.args["db"][collection]  # set collection wanted
        data_cursor = collection.aggregate(pipeline, allowDiskUse=True)
        self.args["data_cursor"] = data_cursor
        return data_cursor

    getCursor.__annotations__ = {"pipeline": str, "return": dict}

    def getBatches(self, batchSize=None):
        """Yield of batches."""
        batchSize = batchSize if batchSize is not None else \
            self.args["db_batch_size"]
        cursor = self.args["data_cursor"]
        # while self.args["data_cursor"]
        if(cursor is not None):
            while(cursor.alive):
                try:
                    yield self.nextBatch(cursor, batchSize)
                except StopIteration:
                    return

    getBatches.__annotations__ = {"pipeline": str, "return": dict}

    def nextBatch(self, cursor, batchSize):
        """Return the very next batch in mongoDb cursor."""
        batch = []
        while(len(batch) < batchSize):
            singleExample = cursor.next()
            batch.append(singleExample)
        return batch

    def __setitem__(self, key, value):
        """Set a single arg or state by, (key, value)."""
        raise NotImplementedError("setitem() is not yet implemented")
        self.args[key] = value

    __setitem__.__annotations__ = {"key": str, "value": any, "return": None}

    def __getitem__(self, key):
        """Get a single arg or state by, (key, value)."""
        raise NotImplementedError("getitem() is not yet implemented")
        try:
            return self.args[key]
        except KeyError:
            return None  # does not exist is the same as None, gracefull catch

    __getitem__.__annotations__ = {"key": str, "return": any}

    def __delitem__(self, key):
        """Delete a single arg or state by, (key, value)."""
        raise NotImplementedError("delitem() is not yet implemented")
        try:
            del self.args[key]
        except KeyError:
            pass  # job is not done but equivalent outcomes so will not error

    __delitem__.__annotations__ = {"key": str, "return": None}

    def __iter__(self):
        """Iterate through housed dictionary, for looping."""
        raise NotImplementedError("iter() is not yet implemented")
        self.db.connect()
        cursor = self.db.getData(pipeline=self.getPipe(
            self.args["pipeline"]), collName=self.args["coll"])

        while(cursor.alive):
            try:
                yield self.nextBatch(cursor)
            except StopIteration:
                return

    __iter__.__annotations__ = {"return": any}

    def __len__(self):
        """Return the first order length of the dictionary."""
        raise NotImplementedError("len() is not yet implemented")
        return len(self.args)

    __len__.__annotations__ = {"return": int}


def _mongo_unit_test():
    import datetime
    """Unit test of MongoDB compat."""
    # create Mongo object to use
    db = Mongo({"test2": 2})
    # output current state of Mongo
    db.debug()
    # stop any active databases already running at the db path location
    db.stop()
    # hold for 2 seconds to give the db time to start
    time.sleep(2)
    # attempt to initialise the database, as in create the database with users
    db.initDb()
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
    db.imports(collection="debug", dictionary={
        "string": "99",
        "number": 99,
        "binary": bin(99),
        "subdict": {"hello": "world"},
        "subarray": [{"hello": "worlds"}, {"hi": "jim"}],
        "timedate": datetime.datetime.utcnow(),
    })
    # log into the database so user can manually check data import
    db.login()
    # attempt to retrieve the data that exists in the collection as a cursor
    db.getCursor(collection="debug", pipeline=[{"$match": {}}])
    # inetate through the data in batches to minimise requests
    for dataBatch in db.getBatches(batchSize=1):
        print(dataBatch)
    db.stop()


if(__name__ == "__main__"):
    _mongo_unit_test()
