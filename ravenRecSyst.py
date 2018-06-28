#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2018-06-28
# @License: Please see LICENSE file in project root



import os, sys, json, inspect, time
from src.helpers import argz, installer, updater, clean, train, test, predict
from src.importer import importData
from src.log import Log



def main():

    # imported here to allow for update first
    from RavenPythonLib.mongodb.mongo import Mongo
    mongodb = Mongo(isDebug=True, mongoUser=args['user'], mongoPath=args['dir'],
        mongoPass=args['pass'], mongoIp=args['ip'], mongoDbName=args['name'],
        mongoCollName="cycles", mongoPort=args['port'], mongoUrl=args['url'])

    if(args["toInitDb"] == True):
        mongodb.debug(print=print) # passing in print to use logger
        mongodb.stop(print=print) # stopping just in case it is already running
        time.sleep(2) # delay to ensure db is closed properly
        mongodb.start(print=print)
        mongodb.addUser(print=print)
        # restart database with new user and with user authentication on
        mongodb.stop(print=print)
        time.sleep(2) # delay to ensure db is closed properly

    if(args["toStartDb"] == True):
        # start main authenticated mongodb service
        mongodb.start(print=print, auth=True)

    # clean + add data if file specified (can be remote)
    if(args["toJustImport"] == True) and (os.path.exists(args["newData"])):
        importData(path=args["newData"], suffix=args["suffix"], mongodb=mongodb,
            chunkSize=args["chunkSize"], print=print)
    elif(os.path.isfile(args["cleaner"]) == True) and (os.path.exists(args["newData"])):
        clean(args=args, print=print)
        importData(path=args["newData"], suffix=args["suffix"], mongodb=mongodb,
         chunkSize=args["chunkSize"], print=print)

    if(args["toTrain"] == True):
        train(print=print)

    if(args["toTest"] == True):
        test(print=print)

    if(None):
        predict(print=print)

    if(args["toStopDb"] == True):
        mongodb.stop(print=print)



# # # # # # # # # #
# following section is just preamble to set some defaults and to update
# # # # # # # # # #



# declaring usefull global variables
home = os.path.expanduser("~")
name = os.path.basename(os.path.abspath(sys.argv[0]))

fileAndPath = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fileAndPath))

prePend = "[ " + name + " ] "
description = name + "; " + "RavenRecSyst, a neural network based recommender system."

dependancies = ["https://github.com/DreamingRaven/RavenPythonLib"]

args = argz(sys.argv[1:], description=description)
args_json = json.loads(json.dumps(args))

# setting fallback logger here pre-update
log = Log(logLevel=args["loglevel"])
print = log.print

# attempting update/ falling back
try: # TODO: devise a method to make erros in nested try, catch
    from RavenPythonLib.updaters.gitUpdate import Gupdater
    nucleon = Gupdater(path=path, urls=dependancies)
    nucleon.install()
    nucleon.update()
    print("main updater success", 3)
except:
    print("Gupdater failed, falling back: " + str(sys.exc_info()[1]), 1)
    installer(path=path, urls=dependancies)
    updater(path=path, urls=dependancies)

# attempting set logger from external lib/ falling back
try:
    from RavenPythonLib.loggers.basicLog import Log
    log = Log(logLevel=args["loglevel"])
    print = log.print # note no '()' as function address desired not itself
    print("main logger success", 3)
except:
    log = Log(logLevel=args["loglevel"])
    print = log.print
    print("Main logger could not be loaded, falling back: " +
        str(sys.exc_info()[1]), 1)

# if >level3 (debug) prepare for some verbose shnitzel
if(args["loglevel"] >= 4):
    main()
else:
    try:
        main()
        # raise ValueError('value x not valid; ...')
        # raise NotImplementedError('not currentley implemented')
    except:
        print(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]), 2)
