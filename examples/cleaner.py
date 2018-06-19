#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-19
# @Filename: cleaner.py
# @Last modified by:   archer
# @Last modified time: 2018-06-19
# @License: Please see LICENSE file in project root
import sys, os, argparse


# this is the file that needs adjusting depending on the needs of the project
def main(args):
    print("Hello, World!")



name = os.path.basename(sys.argv[0])
prePend = "[ " + name + " ] "

def argz(argv=None, description=None):
    if(description == None):
        description = "MongoDb related args"

    parser = argparse.ArgumentParser(description=description)

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
