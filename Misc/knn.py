#!/usr/bin/env python3.6
import time  # realtime
startTime = time.time()

import os
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.neighbors import NearestNeighbors
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split

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

# fourth arg
# setting test/train split
testSize = 0.25  # default value
testSize = float(sys.argv[4]) if len(sys.argv) >= 5 else testSize
print(prePend, "Split test %: ", testSize)

# fifth arg
# setting target name
targetName = "rating"  # default value
targetName = sys.argv[5] if len(sys.argv) >= 6 else targetName
print(prePend, "Target name: ", targetName)

# import data sets
test = pd.read_csv(dataFolderPath + testFileName)  # not used for parameters
train = pd.read_csv(dataFolderPath + trainFileName)  # further split

# remove target in test # tbh its not necessary to store this
#test_noLabel = test[test.columns.difference(['rating'])]

# subsetting training set for validation preventing overfitting on real test
trainTrain, trainTest = train_test_split(train, test_size=testSize)

# debug
#print(test_noLabel.head())

# instantiate model
#knn = KNeighborsClassifier(n_neighbors=3)
knn = KNeighborsRegressor(n_neighbors=3)

# train model
#nnModel = NearestNeighbors(n_neighbors=5, algorithm="ball_tree").fit(train)
# takes a tuple of(X, y) X = training data y = target vals
knn.fit( trainTrain[ trainTrain.columns.difference([targetName]) ],
         trainTrain[targetName])

# find distances to test set / make predictions
#distances, indices = nnModel.kneighbors(test_noLabel)
#pred = knn.predict(test_noLabel)
pred = knn.predict( trainTest[trainTrain.difference([targetName])] )

#print(accuracy_score())

print(prePend, "Fin.", (time.time() - startTime), " seconds.")