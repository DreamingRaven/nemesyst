#!/usr/bin/env python3.6

# modular python file for scatter plots
import pandas as pd
import os
import sys
import struct  # used to accurately calculate python version bits (32/64)
import seaborn as sns

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "
print(prePend, "Purpose: template to ensure consistency.")
print(prePend, "python version (bit): ", struct.calcsize("P") * 8) # check if 32 or 64 bit

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/"  # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# second arg
# setting data file name
dataFileName = "pML.csv"  # default value
dataFileName = sys.argv[2] if len(sys.argv) >= 3 else dataFileName
print(prePend, "Data file name: ", dataFileName)

