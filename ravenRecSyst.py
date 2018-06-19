#!/usr/bin/env python3
# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: app.py
# @Last modified by:   archer
# @Last modified time: 2018-06-19
# @License: Please see LICENSE file in project root



import os, sys, json, inspect, time
from src.helpers import argz, installer, updater, clean
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
    if(os.path.isfile(args["cleaner"]) == True) and (os.path.exists(args["newData"])):
        print("cleaning new files in: " + args["newData"] + " using: "
            + args["cleaner"] + "...", 3)
        clean(print=print)

    # train #TODO: implement selective training
    if(args["toTrain"] == True):
        raise NotImplementedError('Training not currentley implemented')

    # test #TODO: implement complementary testing to training set selection
    if(args["toTest"] == True):
        raise NotImplementedError('Testing not currentley implemented')

    # predict #TODO: selective prediction
    if(None):
        raise NotImplementedError('Predicting not currentley implemented')

    if(args["toStopDb"] == True):
        mongodb.stop(print=print)



#
# following section is just preamble to set some defaults and to update
#

# declaring usefull global variables
home = os.path.expanduser("~")
name = os.path.basename(sys.argv[0])

fileAndPath = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fileAndPath))

prePend = "[ " + name + " ] "
description = name + "; " + "RavenRecSyst entry point."

dependancies = ["https://github.com/DreamingRaven/RavenPythonLib"]

# capture arguments in dict then put into json for bash
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

# if level3 (debug) prepare for some verbose shnitzel
if(args["loglevel"] >= 4):
    main()
else:
    try:
        main()
        # raise ValueError('A very specific bad thing happened.')
        # raise NotImplementedError('not currentley implemented')
    except:
        print(str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]), 2)
