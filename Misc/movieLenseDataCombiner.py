#!usr/bin/env python3.6

# quick python file to wrangle movieLense data set
import pandas as pd
import os
import sys

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/" # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# input data
ratings = pd.read_csv(dataFolderPath + 'pMLRatings.csv')
metadata = pd.read_csv(dataFolderPath + 'pMLMetadata.csv')

# combining data
pML = ratings

# output data
pML.to_csv( (dataFolderPath + "pML.csv"), encoding='utf-8', index=False)

print(prePend, "Fin.")