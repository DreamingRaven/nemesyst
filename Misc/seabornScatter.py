#!/usr/bin/env python3.6

# modular python file for scatter plots
import pandas as pd
import os
import sys
import struct  # used to accurately calculate python version bits (32/64)
import seaborn as sns

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "
print(prePend, "Modular scatter plot visualiser.")
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

# third arg
# Y axis
yName = "rating"  # default value
yName = sys.argv[3] if len(sys.argv) >= 4 else yName
print(prePend, "Y axis: ", yName)

# fourth arg
# X axis
xName = "timestamp"  # default value
xName = sys.argv[4] if len(sys.argv) >= 5 else xName
print(prePend, "X axis: ", xName)

# read in argument selected data
dataSet = pd.read_csv(dataFolderPath + dataFileName)

# plot this shizzle
plot = sns.regplot(x=dataSet[xName], y=dataSet[yName])
plot.plt.show()
plot.savefig("fekme.png")
fig = plot.fig
fig.savefig("shizzle.png")
