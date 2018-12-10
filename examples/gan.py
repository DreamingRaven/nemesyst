#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-12-10
# @License: Please see LICENSE file in project root

import copy
import json
import os
import pickle
import pprint
import sys

import pandas as pd
from keras.layers import (LSTM, Activation, BatchNormalization, Dense,
                          LeakyReLU, Reshape)
from keras.models import Sequential
from keras.utils import plot_model

fileName = "gan.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args


def main(args, db, log):

    # deep copy args to maintain them throught the rest of the program
    args = copy.deepcopy(args)
    log(prePend + "\n\tArg dict of length: " + str(len(args))
        + "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)
    db.connect()
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
        self.model_dict = None
        self.model_cursor = None
        self.prePend = "[ gan.py -> Gan ] "
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(args["tfLogMin"])

    def debug(self):
        self.log(self.prePend, 3)

    def train(self):
        # branch depending if model is to continue training or create new model
        if(self.args["toReTrain"] == True) and (1 == 2):
            # DONT FORGET IF YOU ARE RETRAINING TO CONCATENATE EXISTING STUFF LIKE EPOCHS
            self.model_dict = self.getModel(
                self.getPipe(self.args["modelPipe"]))
            # model is already overwritten when loading from database so self.model != None now
        else:
            self.args["type"] = "gan"
            self.model = self.createModel()
            print(self.model)
        # loop epochs for training

    def test(self, collection=None):
        # uses its own collection variable to allow it to be reused if testColl != coll
        collection = collection if collection is not None else self.args["coll"]
        # branch depending if model is already in memory to save request to database
        if(self.model != None):
            None
        else:
            self.model_dict = self.getModel(
                self.getPipe(self.args["modelPipe"]))
        # now model should exist now use it to test

    def predict(self):
        # branch depending if model is already in memory to save request to database
        if(self.model != None):
            None
        else:
            None

    def save(self):
        None

    # function responsible for creating whatever type of model is desired by the
    # user in this case GANs
    def createModel(self):
        # https://medium.com/@mattiaspinelli/simple-generative-adversarial-network-gans-with-keras-1fe578e44a87        # creating GAN
        # https://github.com/LantaoYu/SeqGAN/blob/master/sequence_gan.py

        generator = self.createGenerator()
        discriminator = self.createDiscriminator()

        generator.compile(
            optimizer=self.args["optimizer"], loss=self.args["lossMetric"])
        # ,  # expand_nested=True
        plot_model(generator, to_file="generator.png")
        # show_shapes=True, dpi=300)
        discriminator.compile(
            optimizer=self.args["optimizer"], loss=self.args["lossMetric"],
            metrics=[self.args["lossMetric"]])
        # ,  # expand_nested=True,
        plot_model(generator, to_file="discriminator.png")
        # show_shapes=True, dpi=300)
        return 0

    def createGenerator(self):
        model = Sequential()
        model.add(Dense(256, input_shape=(100,)))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(self.args["timeSteps"] *
                        self.args["dimensionality"], activation='tanh'))
        model.add(
            Reshape((self.args["timeSteps"], self.args["dimensionality"])))
        model.summary()
        return model

    def createDiscriminator(self):
        model = Sequential()
        # model.add(Flatten(input_shape=self.SHAPE))
        model.add(Dense(self.args["timeSteps"] * self.args["dimensionality"],
                        input_shape=(self.args["timeSteps"], self.args["dimensionality"])))

        model.add(LeakyReLU(alpha=0.2))
        model.add(
            Dense(int((self.args["timeSteps"] * self.args["dimensionality"]) / 2)))
        model.add(LeakyReLU(alpha=0.2))

        model.add(Dense(1, activation='sigmoid'))
        model.summary()
        return model

    def getModel(self, model_pipe=None):
        # modify keras witrh get and set funcs to be able to unserialise the data
        self.make_keras_picklable()
        query = model_pipe if model_pipe is not None else {}
        self.log(self.prePend + "query is: " + str(query) + " giving:", 0)
        # get model cursor to most recent match with query
        self.model_cursor = self.db.getMostRecent(
            query=query, collName=self.args["modelColl"])
        # get a dictionary of key:value pairs of this document from query
        self.model_dict = (
            pd.DataFrame(list(self.model_cursor))
        ).to_dict('records')[0]
        self.model = pickle.loads(self.model_dict["model_bin"])
        self.compile()
        return self.model_dict

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
