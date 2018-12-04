#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-12-04
# @License: Please see LICENSE file in project root

import os
import sys
import json
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
        self.epochs = 0
        self.args = args
        self.model = None
        self.prePend = "[ gan.py -> Gan ]"

    def debug(self):
        self.log(self.prePend, 3)

    def train(self):
        # branch depending if model is to continue training or create new model
        if(self.args["toReTrain"] == True):
            # DONT FORGET IF YOU ARE RETRAINING TO CONCATENATE EXISTING STUFF LIKE EPOCHS
            self.modelDict = self.getModel(
                self.getPipe(self.args["modelPipe"]))
            self.log(self.model, 0)
            None
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

    def getModel(self, model_pipe=None):
        # modify keras witrh get and set funcs to be able to unserialise the data
        self.make_keras_picklable
        query = model_pipe if model_pipe is not None else {}
        return 0

    def getPipe(self, pipePath):
        with open(pipePath) as f:
            return json.load(f)

    def compile(self):
        if(self.model != None):
            self.model.compile(
                optimizer=self.args["optimizer"], loss=self.args["lossMetric"])
        else:
            print("No model to compile, can not NN.compile()", 1)

    def make_keras_picklable(self):
        import tempfile
        import keras.models
        import h5py

        def __getstate__(self):
            model_str = ""
            with tempfile.NamedTemporaryFile(suffix='.hdf5', delete=True) as fd:
                keras.models.save_model(self, fd.name, overwrite=True)
                model_str = fd.read()
                d = {'model_str': model_str}
                return d

        def __setstate__(self, state):
            with tempfile.NamedTemporaryFile(suffix='.hdf5', delete=True) as fd:
                fd.write(state['model_str'])
                fd.flush()
                model = keras.models.load_model(fd.name)
                self.__dict__ = model.__dict__

        cls = keras.models.Model
        cls.__getstate__ = __getstate__
        cls.__setstate__ = __setstate__
