#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-12-02
# @License: Please see LICENSE file in project root

import sys
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

fileName = "gan.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args

def main(args, db, log):

    log( prePend + "\n\tArg dict of length: " + str(len(args)) +
        "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)

    if(args["toTrain"]):
        train(args=args, db=db, log=log)

    if(args["toTest"]):
        test(args=args, db=db, log=log)

    if(args["toPredict"]):
        predict(args=args, db=db, log=log)


def train(args, db, log):
    None




def test(args, db, log):
    None



def predict(args, db, log):
    None
