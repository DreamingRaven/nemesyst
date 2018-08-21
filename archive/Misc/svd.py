#!/usr/bin/env python3.6
import time  # realtime

startTime = time.time()

# quick python file to wrangle movieLense data set
import os
import sys
import struct  # used to accurately calculate python version bits (32/64)
import pandas as pd
from surprise import SVD
from surprise import Dataset
from surprise.model_selection import cross_validate

# creating prepend variable for logging
baseName = os.path.basename(sys.argv[0])  # file name with extension
prePend = "[ " + baseName + " ] "  # prepended to print for debug
fileNameNoExtension = os.path.splitext(baseName)[0]  # file name without extension
print(prePend, "Purpose: calculating eigenvectors and eigenvalues to reduce size and predict missing")
print(prePend, "python version (bit): ", struct.calcsize("P") * 8)  # check if 32 or 64 bit

# outputting more but different debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../DataSets/ml-20m/"  # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# second arg
# setting data file name
dataFileName = "pML.csv"  # default value
dataFileName = sys.argv[2] if len(sys.argv) >= 3 else dataFileName
print(prePend, "Data file name: ", dataFileName)

# simple scikit-surprise usage
data = Dataset.load_builtin('ml-1m')
algo = SVD()  # instantiate model
concatenatedResults = cross_validate(algo, data, measures=['RMSE', 'MAE'], cv=5, verbose=True)

# outputting
results = pd.DataFrame.from_dict(concatenatedResults)
results.to_csv((dataFolderPath + "Model/" + fileNameNoExtension + ".csv"), encoding='utf-8', index=False)

print(prePend, "Fin.", (time.time() - startTime), " seconds.")