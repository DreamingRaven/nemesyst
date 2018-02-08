#!/usr/bin/env python3.6
import time  # realtime
startTime = time.time()

import os
import sys
import pandas as pd
from sklearn.metrics import accuracy_score, mean_absolute_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib  # lib to allow model persistence

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# first arg
# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../DataSets/ml-20m/"  # this is the default path
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

# increasing scope
knn = KNeighborsRegressor(n_neighbors=1)
listResults = []

# for loop which changes k, the number of neighbors to be used
for i in range(1, 20, 3):
    # for loop for repeats of a single k on different data
    for j in range(1, 4):
        k = (i*2)

        # subsetting training set for validation preventing overfitting on real test
        trainTrain, trainTest = train_test_split(train, test_size=testSize)

        # instantiate model at intervals
        knn = KNeighborsRegressor(n_neighbors=k)

        # train model
        knn.fit( trainTrain[ trainTrain.columns.difference([targetName]) ],
                 trainTrain[targetName])

        # find distances to test set / make predictions
        pred = knn.predict( trainTest[trainTrain.columns.difference([targetName])] )

        # output result # first run (0.7786580092802942 MEA)
        MAE = mean_absolute_error(trainTest[targetName], pred)
        print(prePend, "MEA (k =", k, "run =", j, "): ", MAE)
        listResults.append([k, j, MAE])

# combine list of lists into a DataFrame for speed
results = pd.DataFrame(listResults, columns=['k', 'cycle', 'mae'])
print(results)
results.to_csv( (dataFolderPath + "/Model/knn_results.csv"), encoding='utf-8', index=False)

# dump model onto persistent storage
joblib.dump(knn, dataFolderPath + "/Model/knn.pkl")

print(prePend, "Fin.", (time.time() - startTime), " seconds.")