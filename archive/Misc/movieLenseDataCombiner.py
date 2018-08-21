#!/usr/bin/env python3.6
import time  # realtime
startTime = time.time()

# quick python file to wrangle movieLense data set
import pandas as pd
import os
import sys
import struct # used to accurately calculate python version bits (32/64)

# creating prepend variable for logging
prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "
print(prePend, "python version (bit): ", struct.calcsize("P") * 8) # check if 32 or 64 bit

# outputting debug info
cwd = os.getcwd()
print(prePend, "Current wd: ", cwd)
print(prePend, "Args: ", str(sys.argv))

# setting data folder path with possible args(a if condition else b)
dataFolderPath = "../../../DataSets/ml-20m/" # this is the default path
dataFolderPath = dataFolderPath if len(sys.argv) == 1 else sys.argv[1]
print(prePend, "Data path:", dataFolderPath)

# check if data exists
if os.path.isfile(dataFolderPath + "pML.csv"):  # and 1 == 0:
    print(prePend, "pML.csv found... Skipping.")
else: # else generate csv
    print(prePend, "pML.csv not found... Generating.")

    # inputting data
    ratings = pd.read_csv(dataFolderPath + 'pMLRatings.csv')  # TODO: prob's not necessary if other changes below
    metadata = pd.read_csv(dataFolderPath + 'pMLMetadata.csv')

    # combining data
    # sort data to make things more easily debuggable
    metadata.sort_values(['movieId', 'tag'], ascending=[True, True], inplace=True)
    # take every unique tag in metadata and its relevance and add as feature in ratings to its respective movie
    movieTags = metadata.loc[:, ['movieId', 'relevance', 'tag']]  # separate out all information which is not handled
    del metadata  # forcibly cleaning some space
    uniqueTagsMetaData = movieTags['tag'].unique()
    ratingColumnNames = ratings.columns.values.tolist()  # <-- built in fastest method
    eachMoviesTags = movieTags.groupby('movieId')  # head(10) # group by each movie

    # combine column headers into one list #TODO: this is probably not neccessary as lists are combined at modelling
    print(prePend, type(uniqueTagsMetaData.tolist()), type(ratingColumnNames))
    fullFeatureList = ratingColumnNames + uniqueTagsMetaData.tolist() # + user relevance tags

    # creating final (large) data file #TODO: this is probably not neccessary as lists are combined at modelling
    df = pd.DataFrame(columns=fullFeatureList)
    print(prePend, df)

    i = 0                       # not important here only so you can see progress
    x = []                      # list of lists
    specificColumnNames = []    # the specific column names (i.e the tags + movieId)
    for name, group in eachMoviesTags:
        i += 1                                              # increment progress
        groupTemp = group.transpose()                       # transpose to be tag (as column) major order
        groupTemp.columns = groupTemp.iloc[2]               # make a specific row the columns (the tags)
        groupTemp = groupTemp.drop(['tag', 'movieId'], 0)   # remove some rows (old tag column and redundant movieId)
        groupTemp['movieId'] = name                         # add movieId column back in but now without redundancy
        if (i % 10) == 0:                                   # every 10 groups print status
            print(prePend, "progress:", i, "/", len(eachMoviesTags), " movieId: ", groupTemp['movieId'][0])
            if i == 10:                                     # get columns for new dataFrame (here to reduce computation)
                specificColumnNames = groupTemp.columns.tolist()  # copy columns
        x.append(groupTemp.values.tolist())                 # convert group to list, and concat (Faster: list>dataFrame)

    print(prePend, "Useful features of MetaData: ", specificColumnNames)

    # use list of lists 'x' to create dataFrame (trust me this is faster than just using the flat dataFrames!)
    reformedMetaData = pd.DataFrame(x, columns=['lists'])  # single column dataFrame which needs splitting in next step
    reformedMetaData = pd.DataFrame(reformedMetaData['lists'].values.tolist(), columns=specificColumnNames)  # multi col

    # yes yes I know so why even load it? TODO: don't load ratings since unused but keep rename / change name convention
    pML = ratings

    # outputting data
    pML.to_csv( (dataFolderPath + "pML.csv"), encoding='utf-8', index=False)
    reformedMetaData.to_csv(dataFolderPath + "pMLMetaReformed.csv", encoding='utf-8', index=False)

print(prePend, "Fin.", (time.time() - startTime), " seconds.")