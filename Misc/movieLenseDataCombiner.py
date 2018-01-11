#!usr/bin/env python3.6

# quick python file to wrangle movieLense data set
import pandas as pd
import os
import sys
import struct;print(struct.calcsize("P") * 8) # check if 32 or 64 bit

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

# check if data exists
if os.path.isfile(dataFolderPath + "pML.csv"): #and 1 == 0:
    print(prePend, "pML.csv found... Skipping.")
else: # else generate csv
    print(prePend, "pML.csv not found... Generating.")

    # inputting data
    ratings = pd.read_csv(dataFolderPath + 'pMLRatings.csv')
    metadata = pd.read_csv(dataFolderPath + 'pMLMetadata.csv')

    # combining data
    # sort data to make things more easily debuggable
    metadata.sort_values(['movieId', 'tag'], ascending=[True, True], inplace=True)
    # take every unique tag in metadata and its relevance and add as feature in ratings to its respective movie
    movieTags = metadata.loc[:, ['movieId', 'relevance', 'tag']] # separate out all information which is not handled
    del metadata
    uniqueTags = movieTags['tag'].unique()
    #uniqueTags = uniqueTags.to_frame
    eachMoviesTags = movieTags.groupby('movieId')#.head(10) # group by each movie

    print(type(ratings.columns.tolist()), " ello ", type(uniqueTags.tolist()))
    newColumns = ratings.columns.tolist() + uniqueTags.tolist()
    #uniqueTags = uniqueTags.tolist()
    #ratings = ratings.reindex(columns = newColumns)#ratings.columns.tolist() + ['ello']) #+ uniqueTags.tolist())
    print(ratings)

    # create an identical number of null features as previous
    # sort list by time increasing down, and group by user ID
    # For each tag the null = <for each user while in the past> (SUM(tagRelevance * rating))
    pML = ratings

    # outputting data
    pML.to_csv( (dataFolderPath + "pML.csv"), encoding='utf-8', index=False)

print(prePend, "Fin.")