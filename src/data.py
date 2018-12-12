# @Author: George Onoufriou <georgeraven>
# @Date:   2018-12-11
# @Filename: data.py
# @Last modified by:   archer
# @Last modified time: 2018-12-12
# @License: Please see LICENSE in project root.
# @Copyright: George Onoufriou

import os
import sys
import json
import copy
from collections.abc import MutableMapping

# https://medium.freecodecamp.org/how-and-why-you-should-use-python-generators-f6fb56650888


class Data(MutableMapping):
    """
    Data from mongoDb abstract class

    This class is responsible for the high level functionality of the database
    to allow for things like iteration. This is being considered for rolling into
    mongo.py lib file.
    """

    def __init__(self, args, db, log):
        self.args = args
        self.db = db
        self.log = log

    def __delitem__(self):
        raise NotImplementedError("Data.__delitem__() is not yet implemented")

    def __getitem__(self):
        raise NotImplementedError("Data.__getitem__() is not yet implemented")

    def __iter__(self):
        """
        yields subsequent batches of data from mongoDb aggregate pipeline
        """
        self.db.connect()
        cursor = self.db.getData(pipeline=self.getPipe(
            self.args["pipeline"]), collName=self.args["coll"])

        while(cursor.alive):
            try:
                yield self.nextBatch(cursor)
            except StopIteration:
                return

    def nextBatch(self, cursor):
        """
        returns the very next batch in mongoDb cursor
        """
        batch = []
        for unused in range(self.args["batchSize"]):
            batch.append(cursor.next())
        return batch

    def __len__(self):
        raise NotImplementedError("Data.__len__() is not yet implemented")

    def __setitem__(self):
        raise NotImplementedError("Data.__setitem__() is not yet implemented")

    def getPipe(self, pipePath):
        """
        Short func to retrieve pipelines from config files
        """

        with open(pipePath) as f:
            return json.load(f)
