class Mongo(object):

    # imports for whole class (kept between all classes)
    import os
    import sys
    import json

    from pymongo import MongoClient, errors

    # default values which will be set once and unchanged for all Mongo objects
    className = "Mongo"
    prePend = "[ " + os.path.basename(sys.argv[0]) + " -> " + className + "] "

    # default constructor
    def __init__(self, isDebug=None, mongoUser=None, mongoPass=None, mongoIp=None,
                 mongoDbName=None, mongoCollName=None, mongoPort=None, mongoUrl=None):

        # set defaults in non obstructive well defined manner
        self.isDebug = isDebug if isDebug is not None else False
        self.mongoUser = mongoUser if mongoUser is not None else "Groot"
        self.mongoPass = mongoPass if mongoPass is not None else "IamGroot"
        self.mongoIp = mongoIp if mongoIp is not None else "127.0.0.1"
        self.mongoDbName = mongoDbName if mongoDbName is not None else "test"
        self.mongoCollName = mongoCollName if mongoCollName is not None else "testColl"
        self.mongoPort = mongoPort if mongoPort is not None else "27017"
        self.mongoUrl = mongoUrl if mongoUrl is not None else "mongodb://localhost:27017/"
        self.db = None

    def connect(self):
        # set up individual client
        self.client = self.MongoClient(self.mongoUrl,
                                  username=str(self.mongoUser),
                                  password=str(self.mongoPass),
                                  authSource=str(self.mongoDbName),
                                  authMechanism=str('SCRAM-SHA-1'))

        self.db = self.client[self.mongoDbName]

    # check to make sure everything is set properly
    def debug(self):
        print(self.prePend,
              "\n\tDebug = ",       self.isDebug,
              "\n\tUsername = ",    self.mongoUser,
              "\n\tPassword = ",    self.mongoPass,
              "\n\tDb Ip = ",       self.mongoIp,
              "\n\tDb Name = ",     self.mongoDbName,
              "\n\tColl Name =",    self.mongoCollName,
              "\n\tDb Port =",      self.mongoPort,
              "\n\tDb Url =",       self.mongoUrl
              )

    def existanceCheck(self, collName=None):
        # check that db connected
        if (self.db != None):
            nameToCheck = collName if collName is not None else self.mongoCollName

            # display collections
            print(self.prePend, self.db.collection_names())
            if( nameToCheck in self.db.collection_names() ):
                return 1    # if collection exists
            return 0        # if collection does not exist

        else:
            print(self.prePend,
                  "please connect to database using <your Mongo() object>.connect()")
            return 0

    def getData(self, pipeline=None, query=None, collName=None, findOne=False):
        collName = collName if collName is not None else self.mongoCollName

        # check that db connected
        if (self.db != None):

            # check which args are present and call relevant funcs
            if  (findOne == True):
                return self._getDataFindOne(query=query, collName=collName)
            elif(pipeline != None) and (query == None):  # if pipeline used
                return self._getDataThroughPipe(pipeline=pipeline, collName=collName)
            elif(pipeline == None) and (query != None):  # if query used
                return self._getDataThroughFilter(query=query, collName=collName)
            else:
                print(self.prePend,
                      'please provide either a pipeline or query argument')
                return -1
        else:
            print(self.prePend,
                  "please connect to database using <your Mongo() object>.connect()")
            return 0

    def _getDataThroughPipe(self, pipeline, collName):
        collection = self.db[collName]
        return collection.aggregate(pipeline)

    def _getDataThroughFilter(self, query, collName):
        collection = self.db[collName]
        return collection.find(query)

    def _getDataFindOne(self, query, collName):
        collection = self.db[collName]
        return collection.find_one(query)

    def setData(self, data, collName=None):

        if(self.db != None):
            destinationCollection = collName if collName is not None else self.mongoCollName
            # set up collection connection
            collection = self.db[destinationCollection]

            # transform data to json
            jsonPayload = self.json.loads(data.to_json(orient='table'))

            # insert json data
            collection.insert_one(jsonPayload)
        else:
            print(self.prePend,
                  "please connect to database using <your Mongo() object>.connect()")

if __name__ == "__main__":

    import pandas as pd
    #TODO: add unit tests here