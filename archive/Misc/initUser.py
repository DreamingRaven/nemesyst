#!/usr/bin/env python3.6
import time  # realtime
startTime = time.time()

from pymongo import MongoClient
from pymongo import errors

import os
import sys
import argparse

# get home dir && prePend variable for logging
home = os.path.expanduser("~")
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# new shiny magical argument parser HOORAY!
parser = argparse.ArgumentParser(description="automagic user generator for mongoDb")
parser.add_argument("-I", "--ip",   default="127.0.0.1", help="mongod listener, ip address")
parser.add_argument("-N", "--name", default="Test", help="mongo database, name", required=True)
parser.add_argument("-P", "--port", default="27017", help="mongod listener, port")
parser.add_argument("-p", "--pass", default="", help="mongo user, password", required=True)
parser.add_argument("-r", "--role", default="dbOwner", help="mongo user, role", required=True)
parser.add_argument("-U", "--url",  default="mongodb://localhost:27017/", help="mongod/ destination, url")
parser.add_argument("-u", "--user", default="Groot", help="mongo user, username", required=True)

# parser start
args = vars(parser.parse_args())
#print(prePend, "Args: ", args)



try:
    # creating database admin
    print(prePend, "CREATING: ", args['user'], " DB: ", args['name'], " Role: ", args['role'])
    client = MongoClient(args['url'])  # dbUrl)
    db = client[args['name']]
    db.command("createUser", args['user'], pwd=args['pass'], roles=[args['role']])

except OSError as err:

    print(prePend, "OS error: {0}".format(err))

except ValueError:

    print(prePend, sys.exc_info()[0])

except errors.ConnectionFailure:
    print(prePend, "Could not communicate with database: ", sys.exc_info()[0])

except errors.DuplicateKeyError:
    print(prePend, "Error, you are trying to add something that already exists: ", sys.exc_info()[0])
except errors.InvalidName:
    print(prePend, "Error invalid name: (probably username or databaseName)", sys.exc_info()[0])

except:

    # dunno what the error is, may {deity} have mercy on your poor soul
    print(prePend, "unexpected error, mongod could already be running!: ", sys.exc_info()[0])

print(prePend, "Fin.", (time.time() - startTime), " seconds.")