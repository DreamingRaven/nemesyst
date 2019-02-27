#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: lstm.py
# @Last modified by:   archer
# @Last modified time: 2019-02-27
# @License: Please see LICENSE file in project root

"""
Module handler for generative adversarial neural networks
"""

import copy
import datetime
import json
import os
import pickle
import pprint
import sys

import numpy as np
import pandas as pd
from keras.layers import (LSTM, Activation, BatchNormalization, Dense, Flatten,
                          LeakyReLU, Reshape)
from keras.models import Sequential

fileName = "lstm.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args


def main(args, db, log):
    """
    Module entry point

    This entry point deals with the proper invocation of Lstm().
    """

    # deep copy args to maintain them throught the rest of the program
    args = copy.deepcopy(args)
    log(prePend + "\n\tArg dict of length: " + str(len(args))
        + "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)
    db.connect()

    lstm = Lstm(args=args, db=db, log=log)
    lstm.debug()

    if(args["toTrain"]):
        lstm.train()

    if(args["toTest"]):
        lstm.test()

    if(args["toPredict"]):
        lstm.predict()


class Lstm():
    """
    Generative adversarial neural network handler

    This class deals with all abstractions that fascilitate training deep
    neural networks from a MongoDb database object.
    """

    # import protected inside class so that it does not share instances
    from src.data import Data

    def __init__(self, args, db, log):
        self.db = db
        self.log = log
        self.epochs = 0
        self.args = args
        self.model_dict = None
        self.model_cursor = None
        self.prePend = "[ lstm.py -> Lstm ] "
        # this is a dictionary that should be referanced every time something
        # defaults or needs to check what is expected
        self.expected = {
            "type": "lstm",
            "shape": (self.args["batchSize"], self.args["timeSteps"], self.args["dimensionality"]),
        }
        tempArgs = copy.deepcopy(args)
        tempArgs["dimensionality"] = tempArgs["dimensionality"] - 1
        self.data = self.Data(args=tempArgs, db=db, log=log)
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(args["tfLogMin"])

    def debug(self):
        """
        Debug func for displaying class state
        """
        self.log(self.prePend, 3)

    def train(self):
        """
        Func responsible for training certain neural networks

        This func will handle the neccessary clean up and sorting out of
        values and call the correct functions to fully train this network.
        """
        # branch depending if model is to continue training or create new model
        if(self.args["toReTrain"] == True):
            # DONT FORGET IF YOU ARE RETRAINING TO CONCATENATE EXISTING STUFF LIKE EPOCHS
            modelPipe = self.getPipe(self.args["modelPipe"])
            self.model_dict = self.getModel(modelPipe)
            # check that the imported model is a lstm
            # model is already overwritten when loading from database so self.model != None now
        else:
            self.args["type"] = self.expected["type"]
            self.model_dict = self.createModel()
        # show dict to user
        model_json = json.dumps(self.model_dict, indent=4,
                                sort_keys=True, default=str)
        self.log(model_json, 3)

        # TRAINING DISCRIMINATOR on its own
        self.trainer(self.model_dict["discriminator"])

        # TRAINING GENERATOR via full lstm + frozen discriminator
        # self.trainer(self.model_dict["lstm"])

        noise = np.random.normal(
            0, 1, (self.args["batchSize"], self.args["timeSteps"], self.args["dimensionality"]))
        y_mislabeled = np.ones(
            (self.args["batchSize"], self.args["timeSteps"], 1))
        gloss = self.model_dict["lstm"].train_on_batch(noise, y_mislabeled)
        print(gloss)

    def trainer(self, model):
        """
        Responsible for retrieving batches of data and subsequentley training

        This func will be able to handle training a given model with requested
        data batches.
        """
        # for loop that cant step backwards that will iterate the difference
        # between the current epoch of the model and the desired amount
        for epoch in range(self.model_dict["epochs"], self.args["epochs"], 1):
            i = 0
            # loops through database data by returning batches
            for data in self.data:
                documents = pd.DataFrame(data)
                # flattening list
                flat_l = [item for sublist in documents["data"]
                          for item in sublist]
                x = pd.DataFrame(flat_l)
                # while this is the target for other models lstm uses its own
                y = np.repeat(
                    documents["target"], self.args["timeSteps"])
                x["tagret"] = pd.Series(y).values
                realFalse = np.full(
                    (self.args["batchSize"], self.args["timeSteps"], 1), 1)
                x = np.reshape(
                    x.values, (self.args["batchSize"], self.args["timeSteps"], self.args["dimensionality"]))
                # print(pd.DataFrame.from_records(x))
                loss = model.train_on_batch(x, realFalse)
                self.log("epoch: " + str(epoch) + ", batch: " + str(i) +
                    ", length: " + str(len(data)) + ", type: " +
                    str(type(data)) +
                    ", loss: " + str(loss)
                         , 0)
                i += 1

    def test(self, collection=None):
        """
        Func responsible for testing certain neural networks

        This func will attempt retrieval if neural network is not already in
        memory, prior to testing, and will comply to user specified metrics.
        """
        # uses its own collection variable to allow it to be reused if testColl != coll
        collection = collection if collection is not None else self.args["coll"]
        # branch depending if model is already in memory to save request to database
        if(self.model_dict != None):
            None
        else:
            self.model_dict = self.getModel(
                self.getPipe(self.args["modelPipe"]))
        # now model should exist now use it to test

    def predict(self):
        """
        Func responsible for producing predictions for certain neural networks
        """
        # branch depending if model is already in memory to save request to database
        if(self.model_dict != None):
            None
        else:
            None

    def save(self):
        """
        Func responsible for saving the resulting models/ states of models
        """
        None

    # function responsible for creating whatever type of model is desired by the
    # user in this case LSTMs
    def createModel(self):
        """
        Func which creates a generative adversarial model in a dict

        Currentley this is hard coded to be of a specific architecture but this
        can be easily modified and will propogate through should it be
        neccessary.
        """

        # https://medium.com/@mattiaspinelli/simple-generative-adversarial-network-lstms-with-keras-1fe578e44a87
        # https://github.com/LantaoYu/SeqLSTM/blob/master/sequence_lstm.py

        self.log("Generator:", 0)
        generator = self.createGenerator()
        self.log("Discriminator:", 0)
        discriminator = self.createDiscriminator()
        generator.compile(
            optimizer=self.args["optimizer"], loss=self.args["lossMetric"])
        discriminator.compile(
            optimizer=self.args["optimizer"], loss=self.args["lossMetric"],
            metrics=[self.args["lossMetric"]])
        discriminator.trainable = False  # freezing weights

        lstm = Sequential()
        lstm.add(generator)
        lstm.add(discriminator)
        self.log("LSTM:", 0)
        lstm.summary()
        lstm.compile(loss=self.args["lossMetric"],
                     optimizer=self.args["optimizer"])

        try:
            # this is an optional dependancy that is only used for plots
            if(self.args["loglevel"] >= 5):
                from keras.utils import plot_model
                plot_model(generator, to_file="generator.png")
                plot_model(generator, to_file="discriminator.png")
                plot_model(lstm, to_file="LSTM.png")
        except ModuleNotFoundError:
            self.log(
                "ModuleNotFoundError: could not plot models as likeley 'pydot'"
                + " module not found please "
                + " consider installing if you wish to visualise models\n"
                + str(sys.exc_info()[0]) + " "
                + str(sys.exc_info()[1]), 1)

        model_dict = {
            "utc": datetime.datetime.utcnow(),
            "loss": None,
            "epochs": 0,
            "generator": generator,
            "discriminator": discriminator,
            "lstm": lstm,
        }
        return model_dict

    def createGenerator(self):
        """
        Func responsible for creating the generator of a LSTM neural network
        """

        model = Sequential()
        model.add(Dense(256,
                        input_shape=(
                            int(self.args["timeSteps"]), self.args["dimensionality"])
                        ))
        model.add(Flatten())
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(512))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(Dense(1024))
        model.add(LeakyReLU(alpha=0.2))
        model.add(BatchNormalization(momentum=0.8))
        model.add(
            Dense(self.args["timeSteps"] * self.args["dimensionality"], activation='tanh'))
        model.add(
            Reshape((self.args["timeSteps"], self.args["dimensionality"])))
        model.summary()
        return model

    def createDiscriminator(self):
        """
        Func responsible for creating the discriminator of a LSTM neural network
        """

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
        """
        Func which retrieved neural network model from a MongoDb document
        """

        # modify keras witrh get and set funcs to be able to unserialise the data
        self.make_keras_picklable()
        query = model_pipe if model_pipe is not None else {}
        self.log(self.prePend + "db query: " + str(query), 0)
        # get model cursor to most recent match with query
        self.model_cursor = self.db.getMostRecent(
            query=query, collName=self.args["modelColl"])
        # get a dictionary of key:value pairs of this document from query
        model_dict = (
            pd.DataFrame(list(self.model_cursor))
        ).to_dict('records')[0]
        # self.model = pickle.loads(self.model_dict["model_bin"])
        # self.compile()
        if(model_dict["type"] != self.expected["type"]):
            raise RuntimeWarning(
                "The model retrieved using query: " + str(model_pipe)
                + " gives: " + str(model_dict["type"])
                + ", which != expected: " +  self.expected["type"])
        return model_dict

    def getPipe(self, pipePath):
        """
        Short func to retrieve pipelines from config files
        """

        with open(pipePath) as f:
            return json.load(f)

    def make_keras_picklable(self):
        """
        Function which fascilitates serialising keras objects to store as json

        This provides keras with __getstate__ and __setstate__ to be picklable.
        """
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
