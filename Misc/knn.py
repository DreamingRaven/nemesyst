#!usr/bin/env python3.6
import os
import sys
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import numpy as np


# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# first arg
# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/"  # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path: ", dataFolderPath)

# second arg
# setting data file name
testFileName = "test.csv"  # default value
testFileName = sys.argv[2] if len(sys.argv) >= 3 else testFileName
print(prePend, "Test file name: ", testFileName)

# third arg
# setting data file name
trainFileName = "train.csv"  # default value
trainFileName = sys.argv[3] if len(sys.argv) >= 4 else trainFileName
print(prePend, "Train file name: ", trainFileName)

# import data sets
test = pd.read_csv(dataFolderPath + testFileName)
train = pd.read_csv(dataFolderPath + trainFileName)

# train model
nnModel = NearestNeighbors(n_neighbors=2, algorithm="ball_tree").fit(train)

# find distances to test set
distances, indices = nnModel.kneighbors(test)

print(prePend, "Fin.")