#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: NeuralNetwork.py
# @Last modified by:   archer
# @Last modified time: 2018-07-24
# @License: Please see LICENSE file in project root



import pickle
import os, sys
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM



# link for getting distinct values in collection for test train splitting
# http://api.mongodb.com/python/1.4/api/pymongo/collection.html#pymongo.collection.Collection.distinct



class NeuralNetwork():



    home = os.path.expanduser("~")
    fileName = "neuralNetwork"
    prePend = "[ " + fileName + " ] "



    def __init__(self, db, pipeline, args, logger=print):

        self.log = logger
        self.db = db
        self.pipeline = pipeline
        self.args = args
        self.cursor = None
        self.cursorPosition = None
        self.log(self.prePend + "NN.init() success", 3)



    def getCursor(self, pipeline=None):

        if(self.cursor == None) or (pipeline != None):
            pipeline = pipeline if pipeline is not None else self.pipeline
            self.db.connect()
            # can i just point out how smooth the next line is and the complex
            # -ity that is going on behind the scenes
            self.cursor = self.db.getData(pipeline=pipeline)
            self.cursorPosition = 0



    def debug(self):
        self.log(self.prePend       + "\n"  +
                 "\tdb obj: " + str(self.db)  + "\n"  +
                 "\tdb pipeline: " + str(self.pipeline)  + "\n"  +
                 "\tdb cursor: " + str(self.cursor)  + "\n"  +
                 "\tlogger: " + str(self.log),
                 0)


    # this just seeks to control where the model is created from,
    # either retrievef from database or compiled for the first time
    def autogen(self):

        # check cursor has been created atleast before attempting to use it
        if(self.cursor != None):
            # adjust keras so it can save its binary to databases and declare vars
            self.make_keras_picklable()
            self.generateModel()
            self.compile()



    def generateModel(self):
        if( "lstm" == self.args["type"]):
            self.lstm()
        elif("rnn" == self.args["type"]):
            self.rnn()



    def compile(self):

        if(self.model != None):
            self.model.compile(optimizer=self.args["optimizer"], loss=self.args["lossMetric"])
        else:
            print("No model to compile, can not NN.compile()", 1)



# https://machinelearningmastery.com/return-sequences-and-return-states-for-lstms-in-keras/
    def lstm(self):

        model = Sequential()
        bInShape = (1, self.args["timeSteps"], self.args["dimensionality"])

        self.log(
            self.prePend                                                   + "\n" +
            "\t" + "type:\t\t"         + str(self.args["type"])            + "\n" +
            "\t" + "layers:\t\t"       + str(self.args["layers"])          + "\n" +
            "\t" + "timesteps:\t"      + str(self.args["timeSteps"])       + "\n" +
            "\t" + "dimensionality:\t" + str(self.args["dimensionality"])  + "\n" +
            "\t" + "batchSize:\t"      + str(self.args["batchSize"])       + "\n" +
            "\t" + "batchInShape:\t"   + str(bInShape)                     + "\n" +
            "\t" + "activation:\t"     + str(self.args["activation"])      + "\n",
            3
        )

        # gen layers
        for unused in range(self.args["layers"]-1):
            model.add(LSTM(self.args["dimensionality"], activation=self.args["activation"], return_sequences=True, batch_input_shape=bInShape))
        model.add(LSTM(self.args["dimensionality"], activation=self.args["activation"], batch_input_shape=bInShape))
        model.add(Dense(1)) # since regression output is dense 1
        self.model = model
        self.log(self.prePend + "LSTM created", -1)



    def rnn(self):
        model = Sequential()

        self.log(
            self.prePend                                                   + "\n" +
            "\t" + "type:\t\t"         + str(self.args["type"])            + "\n" +
            "\t" + "layers:\t\t"       + str(self.args["layers"])          + "\n" +
            "\t" + "timesteps:\t"      + str(self.args["timeSteps"])       + "\n" +
            "\t" + "dimensionality:\t" + str(self.args["dimensionality"])  + "\n" +
            "\t" + "activation:\t"     + str(self.args["activation"])      + "\n",
            3
        )

        # gen layers
        for unused in range(self.args["layers"]):  # don't need to use iterator just pure loop
            model.add(Dense(self.args["timeSteps"],
                input_dim=self.args["dimensionality"],
                activation=self.args["activation"]))
        model.add(Dense(1)) # this dense 1 is the output layer since this is regression
        self.model = model # if nothing errored now we can assign model
        self.log(self.prePend + "RNN created", -1)



    def loadModel(self):
        None
        raise NotImplementedError('NN.loadModel() not currentley implemented')



    def saveModel(self):
        None
        raise NotImplementedError('NN.saveModel() not currentley implemented')



    #TODO: this should be in mongodb class itself
    def nextDataset(self, batchSize=1):
        data = []
        try:
            # setting batchSize on cursor seems to do nothing
            for unused in range(batchSize):
                document = self.cursor.next()
                data.append(pd.DataFrame(document))

        except StopIteration:
            self.log("cursor has been emptied", -1)
        except ValueError:
            self.log("Value Error: please make sure that something other than \
                plain values are returned by your pipeline e.g include an array \
                of objects then check the following error:" +
                str(sys.exc_info()[0]) + " " +
                str(sys.exc_info()[1]) , 2)
        except:
            self.log(self.prePend + "could not get next data point from mongodb:\n" +
                str(sys.exc_info()[0]) + " " +
                str(sys.exc_info()[1]) , 2)
        return data



    def train(self):

        if(self.model) and (self.cursor):
            self.log("training..." , -1)
            # numSamples = type(self.cursor)

            # keep looping while cursor can give more data
            while(self.cursor.alive):
                dataBatch = self.nextDataset(self.args["batchSize"])
                for inputData in dataBatch:
                    self.log(self.prePend + str(inputData), 0)
                    self.log(self.prePend + str(list(inputData.loc[0, "data"])), 0)
                # self.cursorPosition = self.cursorPosition + self.args["batchSize"]
                # self.log("Im alive " + str(numSamplesTrained) + "/" + str(numSamples), 3)
        else:
            self.log("could not train, either model not generated or cursor does not exist", 2)



    def test(self):
        None
        raise NotImplementedError('NN.test() not currentley implemented')



    def make_keras_picklable(self):
        import keras.models
        import h5py

        def __getstate__(self):
            model_str = ""
            with tempfile.NamedTemporaryFile(suffix='.hdf5', delete=True) as fd:
                keras.models.save_model(self, fd.name, overwrite=True)
                model_str = fd.read()
                d = { 'model_str': model_str }
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
