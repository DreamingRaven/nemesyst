#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-12-03
# @License: Please see LICENSE file in project root

import sys
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

fileName = "gan.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args


def main(args, db, log):

    log(prePend + "\n\tArg dict of length: " + str(len(args)) +
        "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)

    gan = GAN()

    if(args["toTrain"]):
        gan.train()

    if(args["toTest"]):
        gan.test()

    if(args["toPredict"]):
        gan.predict()


class GAN():

    def __init__(self):
        None

    def train(self):
        # if training new model
        # else continuing training
        None

    def test(self):
        # if testing using previously trained model
        # else testing using just-trained model (as in model already in memory)
        None

    def predict(self):
        # if testing using previously trained model
        # else testing using just-trained model (as in model already in memory)
        None
