#!/usr/bin/env python3

# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: RavenRecSyst.py
# @Last modified by:   archer
# @Last modified time: 2019-04-06T19:58:47+01:00
# @License: Please see LICENSE file in project root


import inspect
import json
import os
import sys
import time

from src.aDict import ADict
from src.arg import argz
from src.helpers import (callCustomScript, clean, datetime, installer, updater)
from src.importer import importData
from src.log import Log


def main():

    # imported here as prior to main the program is updated
    from RavenPythonLib.mongodb.mongo import Mongo
    print(args["dir"])

    mongodb = Mongo(isDebug=True, mongoUser=args['user'], mongoPath=args['dir'],
                    mongoPass=args['pass'], mongoIp=args['ip'], mongoDbName=args['name'],
                    mongoCollName=args['coll'], mongoPort=args['port'], mongoUrl=args['url'],
                    mongoCursorTimeout=args['mongoCursorTimeout'])

    if(args["toInitDb"] == True):
        mongodb.debug(print=print)  # passing in print to use logger
        # stopping just in case it is already running
        mongodb.stop(print=print)
        time.sleep(2)  # delay to ensure db is closed properly
        mongodb.start(print=print)
        time.sleep(2)  # similar delay but for startup
        mongodb.addUser(print=print)
        mongodb.stop(print=print)  # stopping database ready for future use
        time.sleep(2)  # delay to ensure db is closed properly

    if(args["toStartDb"] == True):
        # start main authenticated mongodb service
        mongodb.start(print=print, auth=True)
        time.sleep(2)
        mongodb.debug(print=print)

    if(args["toLogin"] == True):
        mongodb.login()

    # clean + add data if file specified (can be remote)
    if(args["toJustImport"] == True) and (len(args["newData"]) >= 1):
        importData(path=args["newData"], suffix=args["suffix"], mongodb=mongodb,
                   chunkSize=args["chunkSize"], print=print)
    elif(os.path.isfile(args["cleaner"]) == True) and (len(args["newData"]) >= 1):
        clean(args=args, print=print)
        importData(path=args["newData"], suffix=args["suffix"], mongodb=mongodb,
                   chunkSize=args["chunkSize"], print=print)

    if(args["type"] == "custom"):
        callCustomScript(args=args, database=mongodb, print=print)

    if(args["toStopDb"] == True):
        time.sleep(2)  # making sure server has time to start
        mongodb.stop(print=print)

    datetime.datetime.utcnow()


# # # # # # # # # #
# following section is just preamble to set some defaults and to update codebase
# # # # # # # # # #


# declaring usefull global variables
name = os.path.basename(os.path.abspath(sys.argv[0]))  # as in this files name
fileAndPath = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fileAndPath))
prePend = "[ " + name + " ] "
description = name + "; " + \
    "Nemesyst, a generalised deep learning framework for server and database model recommendation systems."
dependancies = ["https://github.com/DreamingRaven/RavenPythonLib"]
args = argz(sys.argv[1:], description=description)
# wrap base dict in ADict to make certain issues non-issues
# args = ADict(args)

# setting fallback logger here pre-update
log = Log(logLevel=args["loglevel"])
print = log.print

# attempting update/ falling back
try:  # TODO: devise a method to make erros in nested try, catch
    if(args["toUpdate"] == True):
        from RavenPythonLib.updaters.gitUpdate import Gupdater
        nucleon = Gupdater(path=path, urls=dependancies)
        nucleon.install()
        nucleon.update()
        print(prePend + "main updater success", 3)
    else:
        print(prePend + "Skipping update/ installation since there is no --toUpdate flag given", 0)
except:
    print(prePend + "G-updater failed, try setting --toUpdate flag. falling back: " +
          str(sys.exc_info()[1]), 1)
    installer(path=path, urls=dependancies)
    updater(path=path, urls=dependancies)

# attempting set logger from external lib/ falling back
try:
    from RavenPythonLib.loggers.basicLog import Log
    log = Log(logLevel=args["loglevel"])
    print = log.print  # note no '()' as function address desired not itself
    print(prePend + "main logger success", 3)
except:
    log = Log(logLevel=args["loglevel"])
    print = log.print
    print(prePend + "Main logger could not be loaded, try setting --toUpdate flag. falling back: " +
          str(sys.exc_info()[1]), 1)

# if >level3 (debug) prepare for some verbose shnitzel
if(args["loglevel"] >= 4):
    main()
else:
    try:
        main()
    except ModuleNotFoundError:
        print(prePend + "A dependancy module is missing, try updating using " +
            "'--toUpdate' flag, else 'git pull'. Finally check python " +
            "dependancies exist e.g Keras." +
              str(sys.exc_info()[0]) + " " + str(sys.exc_info()[1]), 2)
    # except:
    #     print(prePend + str(sys.exc_info()[0]
    #                         ) + " " + str(sys.exc_info()[1]), 2)
