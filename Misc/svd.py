#!/usr/bin/env python3.6

# quick python file to wrangle movieLense data set
import pandas as pd
import os
import sys
import struct  # used to accurately calculate python version bits (32/64)
import numpy as np
from scipy.sparse.linalg import svds
from scipy import linalg


# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "
print(prePend, "Purpose: calculating eigenvectors and eigenvalues to reduce size and predict missing")
print(prePend, "python version (bit): ", struct.calcsize("P") * 8)  # check if 32 or 64 bit

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/" # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# second arg
# setting data file name
dataFileName = "pML.csv"  # default value
dataFileName = sys.argv[2] if len(sys.argv) >= 3 else dataFileName
print(prePend, "Data file name: ", dataFileName)

# import data
dataSet = pd.read_csv(dataFolderPath + dataFileName)

# GET IN SHAPE (b-dum ch)
U, s, Vh = svds(dataSet, k=(min(dataSet.shape) - 1))  # min dimension
print(prePend, "(", dataFileName, ").shape = ", dataSet.shape)
print(prePend, "U.shape = ", U.shape)
print(prePend, "s.shape = ", s.shape)
print(prePend, "Vh.shape = ", Vh.shape)

# U, s, Vh = linalg.svd(dataSet)#, k=(min(dataSet.shape) - 1))  # min dimension
# print(prePend, "(", dataFileName, ").shape = ", dataSet.shape)
# print(prePend, "U.shape = ", U.shape)
# print(prePend, "s.shape = ", s.shape)
# print(prePend, "Vh.shape = ", Vh.shape)


# don't be a pain! regenerate the data already Q_Q
#sigma = np.zeros(dataSet.shape)
#for i in range(min(sigma.shape)):
#    sigma[i, i] = s[i]
#a1 = np.dot(U, np.dot(sigma, Vh))
#np.allclose(dataSet, a1)

print(prePend, "Fin.")