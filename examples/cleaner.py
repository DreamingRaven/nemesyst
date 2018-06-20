#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-19
# @Filename: cleaner.py
# @Last modified by:   archer
# @Last modified time: 2018-06-20
# @License: Please see LICENSE file in project root
import sys, os, argparse


# this is the file that needs adjusting depending on the needs of the project
def main(args):

    # insert you're cleaning code here
    # the neccessary arguments are passed to main through "args"
    # you can see each availiable argument in the argz function below
    # to use one of these arguments call it using args["cleaner"]
    # once you have cleaned the files (or not) they will be automagically
    # added to mongodb
    print("Cleaner:", args["cleaner"])
    print("newData:", args["newData"])






def argz(argv, description=None):
    if(description == None):
        description = "MongoDb related args"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-c", "--cleaner",      default="", required=True,
        help="file inclusive path to cleaner file, for data specific cleaning, should also specify --newData")
    parser.add_argument("-d", "--newData",      default="", required=True,
        help="the directory or file of the new data to be added and cleaned, should also specify --cleaner")

    return vars(parser.parse_args(argv))

# setting up to make things nice
name = os.path.basename(sys.argv[0])
prePend = "[ " + name + " ] "

description = str("cleaner file for adaptation to users needs, " +
              "these files deal with data cleaning")

args = argz(sys.argv[1:], description=description)

try:
    main(args=args)
except:
    print(prePend + "could not clean data:\n" +
        str(sys.exc_info()[0]) + " " +
        str(sys.exc_info()[1])
        )
