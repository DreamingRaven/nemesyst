# @Author: George Onoufriou <georgeraven>
# @Date:   2018-12-11
# @Filename: data.py
# @Last modified by:   archer
# @Last modified time: 2019-03-07
# @License: Please see LICENSE in project root.
# @Copyright: George Onoufriou

import copy
import json
import os
import sys
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
        self.warn_count = 0

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
        while(len(batch) < self.args["batchSize"]):
            singleExample = cursor.next()
            # checking shape matches expectations
            if(len(singleExample["data"]) == self.args["timeSteps"]) and \
                    (len(singleExample["data"][0]) == self.args["dimensionality"]):
                # if matches append
                batch.append(singleExample)
            else:
                if(self.warn_count < 10):
                    self.warn_count = self.warn_count + 1
                    self.log("example len: " + str(len(singleExample["data"])) + ", dim: " + str(len(singleExample["data"][0])) + " != " + str(self.args["timeSteps"]) + ", " + str(self.args["dimensionality"]) )
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

    def getSample(self):
        """
        primarily used to check the data is returned
        """
        self.db.connect()
        cursor = self.db.getData(pipeline=self.getPipe(
            self.args["pipeline"]), collName=self.args["coll"])

        while(cursor.alive):
            try:
                return self.nextBatch(cursor)
            except StopIteration:
                return
