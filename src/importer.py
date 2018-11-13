
#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-06-28
# @Filename: importer.py
# @Last modified by:   archer
# @Last modified time: 2018-11-13
# @License: Please see LICENSE file in project root

import os
import sys
import pandas as pd
from fnmatch import fnmatch
from src.helpers import getFileName, getDirPath


def importData(path, suffix, mongodb, chunkSize=10**6, print=print, collName=None):

    # ensuring path is cross platform
    path = os.path.abspath(path)

    if(os.path.isfile(path)):
        filePaths = []
        fileDirPath, file = os.path.split(path)
        importData(path=fileDirPath, suffix=suffix, mongodb=mongodb,
                   chunkSize=chunkSize, print=print)

    elif(os.path.isdir(path)):
        filePaths = []
        pattern = "*" + suffix
        print("importing data: " + str(path) + " " + str(suffix) + " ...", 3)
        # since path points to folder, find all matching files in subdirs
        for path_t, subdirs, files in os.walk(path):
            for name in files:
                # if file name matches a pattern
                if fnmatch(name, pattern):
                    filePath = os.path.join(path_t, name)
                    filePaths.append(filePath)

    else:
        filePaths = []
        raise ValueError(str("Could not find valid files using: " + path + " "
                             + pattern))

    mongodb.connect()

    for filePath in filePaths:
        for chunk in pd.read_csv(filePath, chunksize=chunkSize):
            mongodb.importCsv(filePath, print=print)

            # TODO: current assumption is that each document is already less than
            # 16 MB so then there wont be a need to append to documents but
            # this should probably be additional functionality
