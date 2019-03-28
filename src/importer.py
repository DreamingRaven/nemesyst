#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-28
# @Filename: importer.py
# @Last modified by:   archer
# @Last modified time: 2019-03-05
# @License: Please see LICENSE file in project root

import os
import sys
from fnmatch import fnmatch

import pandas as pd
from src.helpers import getDirPath, getFileName


def importData(path, suffix, mongodb, chunkSize=10**6, print=print, collName=None):

    paths = path
    dirs = []

    # extracting the parent directories involved so that .suffix files can be imported
    for filePath in path:
        filePath = os.path.abspath(filePath)
        if(os.path.isfile(filePath)):
            fileDirPath, file = os.path.split(filePath)
            dirs = dirs + [fileDirPath]
        elif(os.path.isfile(filePath)):
            dirs = dirs + [filePath]
        else:
            print(str(filePath) + " is not file or folder, not imported", 1)

    # using sets to eliminate duplicates in list so multiples files in the same
    # dir dont cause both sets of (.suffix) files to be imported twice
    dirs = list(set(dirs))
    filePaths = []

    # for each directory find children files with *.suffix
    pattern = "*" + str(suffix)

    for dir in dirs:
        for path, subdirs, files in os.walk(dir):
            for name in files:
                if(fnmatch(name, pattern)):
                    filePath = os.path.join(path, name)
                    filePaths.append(filePath)

    mongodb.connect()

    for filePath in filePaths:
        print("importing:" + str(filePath))
        mongodb.importCsv(filePath, print=print)

        # TODO: current assumption is that each document is already less than
        # 16 MB so then there wont be a need to append to documents but
        # this should probably be additional functionality
