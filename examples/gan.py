#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-12-03
# @License: Please see LICENSE file in project root

import os
import sys
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

fileName = "gan.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args


def main(args, db, log):

    log(prePend + "\n\tArg dict of length: " + str(len(args))
        + "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)

    gan = Gan(args=args, db=db, log=log)
    gan.debug()

    if(args["toTrain"]):
        gan.train()

    if(args["toTest"]):
        gan.test()

    if(args["toPredict"]):
        gan.predict()


class Gan():

    def __init__(self, args, db, log):
        self.db = db
        self.log = log
        self.args = args
        self.model = None
        self.prePend = "[ gan.py -> Gan ]"

    def debug(self):
        self.log(self.prePend, 3)

    def train(self):
        # branch depending if model is to continue training or create new model
        if(self.args["toReTrain"] == True):
            None
            # DONT FORGET IF YOU ARE RETRAINING TO CONCATENATE EXISTING STUFF LIKE EPOCHS
        else:
            None
        # loop epochs for training

    def test(self):
        # branch depending if model is already in memory to save request to database
        if(self.model != None):
            None
        else:
            None
        # now model should exist now use it to test

    def predict(self):
        # branch depending if model is already in memory to save request to database
        if(self.model != None):
            None
        else:
            None

    def save(self):
        None
