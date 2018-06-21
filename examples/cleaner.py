#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-19
# @Filename: cleaner.py
# @Last modified by:   archer
# @Last modified time: 2018-06-21
# @License: Please see LICENSE file in project root
import csv, sys, os, argparse
import pandas as pd
import numpy as np

from fnmatch import fnmatch # file matching


# this is the default file called for cleaning, modify this to you're needs,
# or pass call ravenRecSyst with -c argument and specify path to whatever
# cleaning file you have created
def clean(chunk):

    # cleaning code goes here!!!!

    # This should be able to clean on "chunks" which
    # could be portions of files. These chunks are used to ensure that
    # memory usage does not exceed availiable memory
    return chunk.dropna(axis=0)



def main(args):

    # the neccessary arguments are passed to main through "args"
    # you can see each availiable argument in the argz function below
    # to use one of these arguments call it using args["cleaner"]
    # once you have cleaned the files (or not) they will be automagically
    # added to mongodb
    path = os.path.abspath(args["newData"])

    if(os.path.isfile(path)):
        filePaths = [path]

    elif(os.path.isdir(path)):
        filePaths = []
        pattern = "*.csv"
        # since path points to folder, find all matching files in subdirs
        for path_t, subdirs, files in os.walk(path):
            for name in files:
                # if file name matches a pattern
                if fnmatch(name, pattern):
                    filePath = os.path.join(path_t, name)
                    filePaths.append(filePath)

    else:
        filePaths = []
        raise ValueError(str("Could not find valid files using path: " + path))

    for filePath in filePaths:

        suffix = ".data"
        destFilePath = str(filePath + suffix)
        print(prePend + "processing: " + filePath + "\t->\t" + destFilePath)

        # ensure destination file does not already exist
        clearFiles(filePath=destFilePath)

        iteration = 0
        chunkSize = 10 ** 6 # to the power of
        for chunk in pd.read_csv(filePath, chunksize=chunkSize):
            chunk = clean(chunk)
            iteration = iteration + 1
            # chunk.to_csv()



def clearFiles(filePath):
    if(os.path.isfile(filePath)):
        print(prePend + "clearing: " + filePath)
        os.remove(filePath)



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
name = os.path.basename(os.path.abspath(sys.argv[0]))
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
