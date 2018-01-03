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

# import ratings (most important)
filePathRatings = dataFolderPath + 'ratings.csv'
ratings = pd.read_csv(filePathRatings)

# import tags of movies
filePathTags = dataFolderPath + 'tags.csv'
tags = pd.read_csv(filePathTags)

# import tag relevance scores
filePathTagRelevance = dataFolderPath + 'genome-scores.csv'
tagRelevance = pd.read_csv(filePathTagRelevance)

# import tagId to tagName relationship
filePathTagName = dataFolderPath + 'genome-tags.csv'
tagName = pd.read_csv(filePathTagName)

# import movie names
filePathMovieName = dataFolderPath + 'movies.csv'
movieName = pd.read_csv(filePathMovieName)

# merge seperate frames into tags associated to movies
movieTags = pd.merge(tagRelevance, tagName)
# merge tags with movies and genres
movieMetaData = pd.merge(movieTags, movieName)

movieMetaData.sort_values(['movieId', 'relevance'], ascending=[True, False], inplace=True)
topXTags = movieMetaData.groupby('movieId').head(10)
userAvgRating = ratings.groupby('userId')['rating'].mean()

# check if users line up
numUsers = len(set(ratings['userId']))
numUserRatings = len(userAvgRating)
lastUserId = (ratings.tail(1).iloc[0])[0]
listUniqueUsers = list(ratings['userId'].unique())

# check if movies line up first reorder the list
ratings.sort_values(['movieId', 'userId'], ascending=[True, False], inplace=True) # this changes order for movies so cannot recombine
movieAvgRating = ratings.groupby('movieId')['rating'].mean()
numMovies = len(set(ratings['movieId']))
numMovieRatings = len(movieAvgRating)
lastMovieId = (ratings.tail(1).iloc[0])[1] #fek
listUniqueMovies = list(ratings['movieId'].unique())

# user avg ratings as data frame
userAvgRatingWithId = pd.DataFrame()
userAvgRatingWithId['userAvgRating'] = userAvgRating
userAvgRatingWithId['userId'] = listUniqueUsers

# movie avg ratings as data frame
movieAvgRatingWithId = pd.DataFrame()
movieAvgRatingWithId['movieAvgRating'] = movieAvgRating
movieAvgRatingWithId['movieId'] = listUniqueMovies

ratings = pd.merge(ratings, movieAvgRatingWithId)
ratings = pd.merge(ratings, userAvgRatingWithId)

ratings.sort_values(['movieId', 'userId'], ascending=[True, True], inplace=True)
#rating_tags = pd.merge(ratings, tags)

# check if data sets exist if not, generate.
if os.path.isfile(dataFolderPath + "pMLRatings.csv"):
    print(prePend, "pMLRatings.csv found... Skipping.")
else:
    print(prePend, "pMLRatings.csv not found... Generating.")
    ratings.to_csv( (dataFolderPath + "pMLRatings.csv"), encoding='utf-8', index=False)

if os.path.isfile(dataFolderPath + "pMLMetadata.csv"):
    print(prePend, "pMLMetadata.csv found... Skipping.")
else:
    print(prePend, "pMLMetadata.csv not found... Generating.")
    movieMetaData.to_csv( (dataFolderPath + "pMLMetadata.csv"), encoding='utf-8', index=False)

#ratings.to_csv( (dataFolderPath + "pMLRatings.csv"), encoding='utf-8', index=False)
#movieMetaData.to_csv( (dataFolderPath + "pMLMetadata.csv"), encoding='utf-8', index=False)

print(prePend, "Fin.")
