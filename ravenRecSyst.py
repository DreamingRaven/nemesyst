#!/usr/bin/env python3
# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-16
# @Filename: app.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-05-29
# @License: Please see LICENSE file in project root



import os, sys, inspect
from src.miscHelpers import argz, installer, updater
from posixpath import basename, dirname




# setting for ease of debug output
home = os.path.expanduser("~")
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

fileAndPath = inspect.getframeinfo(inspect.currentframe()).filename
path = os.path.dirname(os.path.abspath(fileAndPath))



def main():
    print(args, 3)

    if args["verbose"] <=2:
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '0'

    # start instance of database
    if args["toInitDb"] == True:
        None
    # clean specified data + add to database
    if args["clean"] != "":
        print(args["clean"])



# getting arguments
args = argz(sys.argv[1:])

# updating libs from url list
urls = ["https://github.com/DreamingRaven/RavenPythonLib"]
installer(path=path, urls=urls)
updater(path=path, urls=urls)

# using logger from libs
try:
    from RavenPythonLib.loggers.basicLog import Log
    log = Log(logLevel=args["verbose"])
    print = log.print # overloading print with own logger

except:
    print(prePend + " [ warning ] " + "could not use logger, falling back.")

main()
