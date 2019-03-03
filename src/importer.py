
#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-28
# @Filename: importer.py
# @Last modified by:   archer
# @Last modified time: 2019-03-03
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

    # print(filePaths)

    # for filePath in paths:
    #     # ensuring path is cross platform
    #     filePath = os.path.abspath(filePath)
    #
    #     if(os.path.isfile(filePath)):
    #         filePaths = []
    #         fileDirPath, file = os.path.split(filePath)
    #         importData(path=[fileDirPath], suffix=suffix, mongodb=mongodb,
    #                    chunkSize=chunkSize, print=print)
    #
    #     elif(os.path.isdir(filePath)):
    #         filePaths = []
    #         pattern = "*" + suffix
    #         print("importing data: " + str(filePath)
    #               + " " + str(suffix) + " ...", 3)
    #         # since path points to folder, find all matching files in subdirs
    #         for path_t, subdirs, files in os.walk(filePath):
    #             for name in files:
    #                 # if file name matches a pattern
    #                 if fnmatch(name, pattern):
    #                     filePath = os.path.join(path_t, name)
    #                     filePaths.append(filePath)
    #
    #     else:
    #         filePaths = []
    #         raise ValueError(str("Could not find valid files using: " + filePath + " "
    #                              + pattern))
    #
    mongodb.connect()

    for filePath in filePaths:
        mongodb.importCsv(filePath, print=print)

    # for filePath in filePaths:
    #         for chunk in pd.read_csv(filePath, chunksize=chunkSize):
    #             mongodb.importCsv(filePath, print=print)

        # TODO: current assumption is that each document is already less than
        # 16 MB so then there wont be a need to append to documents but
        # this should probably be additional functionality
