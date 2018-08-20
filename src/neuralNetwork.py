#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: NeuralNetwork.py
# @Last modified by:   archer
# @Last modified time: 2018-08-20
# @License: Please see LICENSE file in project root


import pickle
import os, sys
import pandas as pd
import numpy as np
import datetime
from bson import objectid, Binary
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM



# link for getting distinct values in collection for test train splitting
# http://api.mongodb.com/python/1.4/api/pymongo/collection.html#pymongo.collection.Collection.distinct



class NeuralNetwork():



    home = os.path.expanduser("~")
    fileName = "neuralNetwork"
    prePend = "[ " + fileName + " ] "



    def __init__(self, db, pipeline, args, logger=print):

        self.db = db
        self.args = args
        self.log = logger
        self.cursor = None
        self.history = None
        self.pipeline = pipeline
        self.cursorPosition = None
        self.log(self.prePend + "NN.init() success", 3)
        self.sumError = None
        self.numExamples = None
        self.numValidExamples = None
        # control shutting up tensorflow
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(args["tfLogMin"])



    def getCursor(self, pipeline=None):

        if(self.cursor == None) or (pipeline != None):
            pipeline = pipeline if pipeline is not None else self.pipeline
            self.db.connect()
            # can i just point out how smooth the next line is and the complex
            # -ity that is going on behind the scenes
            self.cursor = self.db.getData(pipeline=pipeline)
            self.cursorPosition = 0
            # this is to allow a higher try catch to delete it
            return self.cursor
        else:
            self.log(prePend + "could not generate cursor as cursor already exists or no pipeline is provided", 1)



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



    def lstm(self):

        model = Sequential()
        #TODO: off by one error please for the love of god george
        bInShape = (1, self.args["timeSteps"]+1, self.args["dimensionality"])

        self.log(
            self.prePend                                                   + "\n" +
            "\t" + "type:\t\t"         + str(self.args["type"])            + "\n" +
            "\t" + "layers:\t\t"       + str(self.args["layers"])          + "\n" +
            "\t" + "timesteps:\t"      + str(self.args["timeSteps"])       + "\n" +
            "\t" + "dimensionality:\t" + str(self.args["dimensionality"])  + "\n" +
            "\t" + "batchSize:\t"      + str(self.args["batchSize"])       + "\n" +
            "\t" + "batchInShape:\t"   + str(bInShape)                     + "\n" +
            "\t" + "epochs:\t\t"       + str(self.args["epochs"])          + "\n" +
            "\t" + "activation:\t"     + str(self.args["activation"])      + "\n",
            0
        )

        # gen layers
        for unused in range(self.args["layers"]-1):
            model.add(LSTM(self.args["dimensionality"], activation=self.args["activation"], return_sequences=True, batch_input_shape=bInShape))
        model.add(LSTM(self.args["dimensionality"], activation=self.args["activation"], batch_input_shape=bInShape))
        model.add(Dense(1))
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
            "\t" + "epochs:\t\t"       + str(self.args["epochs"])          + "\n" +
            "\t" + "activation:\t"     + str(self.args["activation"])      + "\n",
            0
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



    #TODO: this should be in mongodb class itself
    def nextDataset(self, batchSize=1):
        data = []
        try:
            # setting batchSize on cursor seems to do nothing
            for unused in range(batchSize):
                document = self.cursor.next()
                data.append(document)
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
        self.modler(toTrain=True)
        self.log(self.prePend +
            "\n\tsumError: " + str(self.sumError) +
            " \n\tnumExamples: " + str(self.numExamples) +
            " \n\tnumValidExamples " + str(self.numValidExamples) +
            " \n\tmeanError: " + str(self.sumError / self.numValidExamples),
            0)
        # save the resulting model
        self.saveModel()


    def test(self):
        self.modler(toTrain=False)
        self.log(self.prePend +
            "\n\tsumError: " + str(self.sumError) +
            " \n\tnumExamples: " + str(self.numExamples) +
            " \n\tnumValidExamples " + str(self.numValidExamples) +
            " \n\tmeanError: " + str(self.sumError / self.numValidExamples),
            0)


    # the universal interface that allows the code of both test and train to be
    # one single set. "Don't repeat yourself"
    def modler(self, toTrain=None):
        sumError = 0
        numExamples = 0
        self.numValidExamples = 0


        # check if model exists and that cursor exists
        if(self.model) and (self.cursor):

            if(toTrain == True):
                self.log("training on " + self.args["coll"] + " ..." , -1)
            else:
                self.log("testing on "  + self.args["coll"] + " ..." , -1)


            # keep looping while cursor can give more data
            while(self.cursor.alive):
                dataBatch = self.nextDataset(1)
                for mongoDoc in dataBatch:
                    numExamples = numExamples + 1
                    #TODO this is fine if both are pushed lists
                    data = pd.DataFrame(list(mongoDoc["data"]))
                    data = np.expand_dims(data.values, axis=0)

                    #TODO needs generalisation for many to many or one to many
                    target = mongoDoc["target"]
                    target = np.full((1, 1), target)

                    if(toTrain == True):
                        self.testTrainer(data=data, target=target,
                            id=mongoDoc["_id"], toTrain=True)
                    else:
                        try:
                            sumError = sumError + self.testTrainer(data=data,
                                target=target, id=mongoDoc["_id"], toTrain=False)
                        except TypeError:
                            self.log("NN.testTrainer returned nothing" +
                                str(sys.exc_info()[0]) + " " +
                                str(sys.exc_info()[1]), 3)

            if(toTrain == True):
                # cursor is now dead so make it None
                self.cursor = None
                # since this is training we need training accuracy so need to regen cursor
                self.getCursor()
                # call self again but to test now
                self.modler(toTrain=False)
            else:
                self.sumError = sumError
                self.numExamples = numExamples
        else:
            if(toTrain == True):
                self.log("could not train, either model not generated or cursor does not exist" , 2)
            else:
                self.log("could not test, either model not generated or cursor does not exist..." , -1)



    def testTrainer(self, data, target, id, toTrain=False):
        try:
            #TODO: off by one ... you fool george, sort this out
            expectShape = (1, self.args["timeSteps"] + 1, self.args["dimensionality"])

            # check if shape meets expectations
            if(data.shape == expectShape):

                if(toTrain == True):
                    # self.model.summary()
                    self.model.fit(x=data, y=target, batch_size=self.args["batchSize"],
                        epochs=self.args["epochs"], verbose=self.args["kerLogMax"],
                        callbacks=None, validation_split=0, validation_data=None,
                        shuffle=False, class_weight=None, sample_weight=None,
                        initial_epoch=0, steps_per_epoch=None, validation_steps=None)
                else:
                    self.numValidExamples = self.numValidExamples + 1
                    return self.model.evaluate(x=data, y=target,
                        batch_size=self.args["batchSize"],
                        verbose=self.args["kerLogMax"])

            else:
                self.log(self.prePend + str(id) + " " + str(data.shape) + " != "
                    + str(expectShape), 1)
                return 0

        except:
            if(self.args["toTrain"]):
                self.log(self.prePend + "could not train:\t" + str(id) + "\n" +
                    str(sys.exc_info()[0]) + " " +
                    str(sys.exc_info()[1]), 2)
            else:
                self.log(self.prePend + "could not test:\t" + str(id) + "\n" +
                    str(sys.exc_info()[0]) + " " +
                    str(sys.exc_info()[1]), 2)



    def saveModel(self):
        if(self.model != None):
            stateDict = self.args
            stateDict["pipe"] = str(self.pipeline)
            del stateDict["pass"]
            stateDict["utc"] = datetime.datetime.utcnow()
            if(self.sumError):
                stateDict["sumError"] = self.sumError
            if(self.numExamples):
                stateDict["numSamples"] = self.numExamples
            if(self.numValidExamples):
                stateDict["numValidSamples"] = self.numValidExamples
            if(self.sumError) and (self.numValidExamples):
                stateDict["meanError"] = self.sumError / self.numValidExamples
            # save model
            self.make_keras_picklable()
            model_bytes = pickle.dumps(self.model)
            stateDict['model_bin'] = Binary(model_bytes)

            self.db.shoveJson(stateDict, collName=str(self.args["modelColl"]))



    def make_keras_picklable(self):
        import tempfile
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
