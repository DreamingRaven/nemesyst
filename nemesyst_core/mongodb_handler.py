# @Author: George Onoufriou <archer>
# @Date:   2019-07-15
# @Email:  george raven community at pm dot me
# @Filename: mongo_compat.py
# @Last modified by:   archer
# @Last modified time: 2019-08-03
# @License: Please see LICENSE in project root

from __future__ import print_function, absolute_import   # python 2-3 compat
import os
import subprocess
import time
from pymongo import MongoClient, errors  # python 2 or python 3 versions


class Mongo(object):
    """Python2/3 compatible MongoDb utility wrapper.

    This wrapper saves its state in an internal overridable dictionary
    such that you can adapt it to your requirements, if you should need to do
    something unique, the caveat being it becomes harder to read.
    """

    def __init__(self, args=None, logger=None):
        """Init class with defaults.

        optionally accepts dictionary of default overides.
        """
        args = args if args is not None else dict()
        self.home = os.path.expanduser("~")
        defaults = {
            "mongoUser": "groot",
            "mongoPass": "iamgroot",
            "mongoAuth": "SCRAM-SHA-1",
            "userRole": "readWrite",
            "mongoIp": "127.0.0.1",
            "mongoDbName": "RecSyst",
            "mongoCollName": "testColl",
            "mongoPort": "27017",
            # "mongoUrl": "mongodb://localhost:27017/",
            "mongoPath": self.home + "/db",
            "mongoLogPath": self.home + "/db" + "/log",
            "mongoLogName": "mongoLog",
            "mongoCursorTimeout": 600000,
            "mongoBatchSize": 32,
            "pylog": logger if logger is not None else print,
            "mongoSsl": None,
            "db": None,
            "mongoPipeline": None,
        }
        self.args = self._merge_dicts(defaults, args)
        # final adjustments to newly defined dictionary
        self.args["mongoUrl"] = "mongodb://{0}:{1}/".format(
            self.args["mongoIp"], self.args["mongoPort"])

    __init__.__annotations__ = {"args": dict, "return": None}

    def test(self):
        """This is a docstring."""
        pass
    test.__annotations__ = {"return": None}

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
            str(self.args["mongoPath"]),
            str(self.args["mongoLogPath"]),
        ])
        cliArgs = [  # non authentication version of db start
            "mongod",
            "--bind_ip",        "127.0.0.1",
            "--port",           "27017",
            "--dbpath",         str(self.args["mongoPath"]),
            "--logpath",        str(self.args["mongoLogPath"] +
                                    self.args["mongoLogName"]),
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

    def connect(self):
        """Connect to a specific mongodb database defined in args.

        Uses mongoUrl, mongoUser, mongoPass, mongoDbName.
        """
        self.args["client"] = MongoClient(
            self.args["mongoUrl"],
            username=str(self.args["mongoUser"]),
            password=str(self.args["mongoPass"]),
            authSource=str(self.args["mongoDbName"]),
            authMechanism=str(self.args["mongoAuth"]))
        self.args["db"] = self.args["client"][self.args["mongoDbName"]]

    connect.__annotations__ = {"return": None}

    def login(self):
        """Log in to database, interupt, and availiable via cli."""
        loginArgs = [
            "mongo",
            "--port", str(self.args["mongoPort"]),
            "-u",   str(self.args["mongoUser"]),
            "-p", str(self.args["mongoPass"]),
            "--authenticationDatabase", str(self.args["mongoDbName"])
        ]
        subprocess.call(loginArgs)

    login.__annotations__ = {"return": None}

    def start(self):
        """Launch the database."""
        self.args["pylog"]("Starting mongodb: auth=",
                           str(self.args["mongoAuth"]))
        cliArgs = [
            "mongod",
            "--bind_ip",        str(self.args["mongoIp"]),
            "--port",           str(self.args["mongoPort"]),
            "--dbpath",         str(self.args["mongoPath"]),
            "--logpath",        str(self.args["mongoLogPath"] +
                                    self.args["mongoLogName"]),
            "--setParameter",   str("cursorTimeoutMillis=" +
                                    str(self.args["mongoCursorTimeout"])),
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
             "--dbpath", str(self.args["mongoPath"]),
             "--shutdown"]
        )

    stop.__annotations__ = {"return": None}

    def _addUser(self):
        """Add a user with given permissions to the authentication database."""
        self.args["pylog"]("Adding  mongodb user:",
                           str(self.args["mongoUser"]),
                           ", role:", str(self.args["userRole"]),
                           ", authdb:", str(self.args["mongoDbName"]))
        client = MongoClient("mongodb://localhost:27017/")
        db = client[self.args["mongoDbName"]]
        try:
            if(self.args["userRole"] == "all"):
                db.command("createUser",
                           self.args["mongoUser"],
                           pwd=self.args["mongoPass"],
                           roles=["readWrite", "dbAdmin"])
            else:
                db.command("createUser",
                           self.args["mongoUser"],
                           pwd=self.args["mongoPass"],
                           roles=[self.args["userRole"]])
        except errors.DuplicateKeyError:
            self.args["pylog"](self.args["mongoUser"] + "@" +
                               self.args["mongoDbName"],
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
            self.args["mongoPipeline"]
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
            self.args["mongoBatchSize"]
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


def test():
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
    test()
