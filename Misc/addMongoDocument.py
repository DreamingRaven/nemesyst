#!/usr/bin/env python3.6
import time  # realtime
startTime = time.time()

from pymongo import MongoClient
from pymongo import errors
from numpy import genfromtxt

import os
import sys
import json
import argparse
import pandas as pd
from pandas import errors as e

# setting for ease of debug output
home = os.path.expanduser("~")
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# new shiny magical argument parser HOORAY!
parser = argparse.ArgumentParser(description="populate mongo database with more .csv data")
parser.add_argument("-C", "--coll", default="testColl", help="collection name to which data is to be added")
parser.add_argument("-D", "--data", help="csv data paths to be added (space separated if multiple)", required=True)
parser.add_argument("-I", "--ip",   default="127.0.0.1", help="mongod listener, ip address")
parser.add_argument("-N", "--name", default="test", help="mongo database, name", required=True)
parser.add_argument("-P", "--port", default="27017", help="mongod listener, port")
parser.add_argument("-p", "--pass", default="i am groot", help="mongo user, password", required=True)
parser.add_argument("-U", "--url",  default="mongodb://localhost:27017/", help="mongod/ destination, url")
parser.add_argument("-u", "--user", default="Groot", help="mongo user, username", required=True)

# parser start
args = vars(parser.parse_args())

try:
    print(prePend, "Connecting to mongoDb: ", args['url'], args['name'], args['coll'])

    # connect to db
    client = MongoClient(args['url'], username=args['user'], password=args['pass'],
                         authSource=args['name'], authMechanism='SCRAM-SHA-1')

    db = client[args['name']]
    collection = db[args['coll']]

    counter = 0

    # unfortunately loop needed since small adjustments must be made
    for file in args['data'].splitlines():

        # print(file)
        try:
            # numpy-load is faster but pd is slower for more usability, same story with 'table'
            jsonPayload = json.loads(pd.read_csv(file).to_json(orient='records'))
            print(jsonPayload)
            print()
            collection.insert_one(jsonPayload)
        except e.EmptyDataError:
            print("Empty: ", sys.exc_info()[0], file)
        except:
            print("could not import to mongo", sys.exc_info()[0])

        counter += 1

    print(counter)

except OSError as err:

    print(prePend, "OS error: {0}".format(err))

except ValueError:

    print(prePend, sys.exc_info()[0])

except errors.ConnectionFailure:
    print(prePend, "Could not communicate with database/ communication interrupted: ", sys.exc_info()[0])

except errors.DuplicateKeyError:
    print(prePend, "Error, you are trying to add something that already exists: ", sys.exc_info()[0])

except:

    # dunno what the error is, may {deity} have mercy on your poor soul
    print(prePend, "unexpected error, mongod could already be running!: ", sys.exc_info()[0])

print(prePend, "Fin.", (time.time() - startTime), " seconds.")

print(prePend, "Fin.", (time.time() - startTime), " seconds.")

#
# testCollectionDocument = {"author": "theBezt",
#                           "text": "2Spoopy4you",
#                           "pythonList": ["1", "2", "three"],
#                           "date": datetime.datetime.utcnow()
#                           }
# documentId = collection.insert_one(testCollectionDocument).inserted_id
# print(documentId)