#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: NeuralNetwork.py
# @Last modified by:   archer
# @Last modified time: 2018-11-13
# @License: Please see LICENSE file in project root


import pickle
import os
import sys
import pprint
import copy
import pandas as pd
import numpy as np
import datetime
from bson import objectid, Binary
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM


class NeuralNetwork():

    home = os.path.expanduser("~")
    fileName = "neuralNetwork"
    prePend = "[ " + fileName + " ] "

    def __init__(self, db, data_pipeline, args, model_pipeline=None, logger=print, model=None, currentEpoch=None):

        self.db = db
        self.args = args
        self.log = logger
        self.model = model if model is not None else None
        self.cursor = None
        self.history = None
        self.sumError = None
        self.numExamples = None
        self.data_pipeline = data_pipeline
        self.model_pipeline = model_pipeline  # can be None
        self.numValidExamples = None
        self.log(self.prePend + "NN.init() success", 3)
        self.model_dict = None
        self.currentEpoch = currentEpoch if currentEpoch is not None else 0
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = str(args["tfLogMin"])

    def getCursor(self, pipeline=None, collName=None):

        if(self.cursor == None) or (pipeline != None):
            pipeline = pipeline if pipeline is not None else self.data_pipeline
            collName = collName if collName is not None else self.args["coll"]
            self.db.connect()
            self.cursor = self.db.getData(pipeline=pipeline, collName=collName)
            # this is to allow a higher try catch to delete it
            return self.cursor
        else:
            self.log(
                prePend + "could not generate cursor as cursor already exists or no pipeline is provided", 1)

    def debug(self):
        self.log(self.prePend + "\n" +
                 "\tdb obj: " + str(self.db) + "\n" +
                 "\tdb pipeline: " + str(self.data_pipeline)  + "\n" +
                 "\tdb cursor: " + str(self.cursor)  + "\n" +
                 "\tlogger: " + str(self.log),
                 0)

    # automagic model generation

    def autogen(self):
        if(self.cursor != None) and (self.model == None):
            self.generateModel()
            self.compile()

    # TODO: check this through yet untested

    def getModel(self):
        if(self.model == None):
            self.make_keras_picklable()
            query = {}
            if(self.model_pipeline != None):
                query = self.model_pipeline

            self.log(self.prePend + "query is: " + str(query), 0)
            # attempt to get model using cursor
            model_cursor = self.db.getMostRecent(
                query=query, collName=self.args["modelColl"])

            if(model_cursor != None):
                model_metadata = pd.DataFrame(list(model_cursor))
                self.model_dict = model_metadata.to_dict('records')
                if(self.model_dict != []):
                    # no one wants to see the binary
                    del self.model_dict[0]["model_bin"]
                    self.log(self.prePend + "Loading model:", 0)
                    pprint.pprint(self.model_dict)
                    model_bin = dict(model_metadata['model_bin'])[0]
                    self.model = pickle.loads(model_bin)
                    self.compile()
                else:
                    self.log(self.prePend + "retrieved document is empty/ does not exist likeley bad query: document_metadata="
                             + str(model_metadata) + "\ndocument_dict=" + str(self.model_dict), 2)
            else:
                self.log(self.prePend +
                         "could not get model cursor from database: ", 2)
        else:
            self.log(self.prePend +
                     "model already in memory skipping retrieval", 0)

    def generateModel(self):
        if("lstm" == self.args["type"]):
            self.model = self.lstm()
        elif("rnn" == self.args["type"]):
            self.model = self.rnn()

    def compile(self):
        if(self.model != None):
            self.model.compile(
                optimizer=self.args["optimizer"], loss=self.args["lossMetric"])
        else:
            print("No model to compile, can not NN.compile()", 1)

    def lstm(self):
        model = Sequential()
        bInShape = (1, self.args["timeSteps"], self.args["dimensionality"])

        self.log(
            self.prePend + "\n"
            + "\t" + "type:\t\t"         + str(self.args["type"])            + "\n"
            + "\t" + "layers:\t\t"       + str(self.args["layers"])          + "\n"
            + "\t" + "timesteps:\t"      + str(self.args["timeSteps"])       + "\n"
            + "\t" + "dimensionality:\t" + str(self.args["dimensionality" ])  + "\n"
            + "\t" + "batchSize:\t"      + str(self.args["batchSize"])       + "\n"
            + "\t" + "batchInShape:\t"   + str(bInShape)                     + "\n"
            + "\t" + "epochs:\t\t"       + str(self.args["epochs"])          + "\n"
            + "\t" + "epochs_chunk:\t"   + str(self.args["epochs_chunk"])    + "\n"
            + "\t" + "activation:\t"
            + str(self.args["activation" ])      + "\n",
            0
        )

        # gen layers
        for unused in range(self.args["layers"] - 1):
            model.add(LSTM(self.args["intLayerDim"], activation=self.args["activation"],
                           return_sequences=True, batch_input_shape=bInShape))
        model.add(LSTM(
            self.args["intLayerDim"], activation=self.args["activation"], batch_input_shape=bInShape))
        model.add(Dense(1))
        self.log(self.prePend + "LSTM created", -1)
        return model

    def rnn(self):
        model = Sequential()

        self.log(
            self.prePend + "\n"
            + "\t" + "type:\t t"         + str(self.args["type"])            + "\n"
            + "\t" + "layers:\t t"       + str(self.args["layers"])          + "\n"
            + "\t" + "timesteps: t"      + str(self.args["timeSteps"])       + "\n"
            + "\t" + "dimensionality:\t" + str(self.args["dimensionality" ])  + "\n"
            + "\t" + "epochs:\t t"       + str(self.args["epochs"])          + "\n"
            + "\t" + "activation: t"
            + str(self.args["activation" ])      + "\n",
            0
        )

        # gen layers
        # don't need to use iterator just pure loop
        for unused in range(self.args["layers"]):
            model.add(Dense(self.args["timeSteps"],
                            input_dim=self.args["dimensionality"],
                            activation=self.args["activation"]))
        # this dense 1 is the output layer since this is regression
        model.add(Dense(1))
        self.log(self.prePend + "RNN created", -1)
        return model  # if nothing errored now we can assign model

    # TODO: this should be in mongodb class itself

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

    def getNewDatabase(self):
        from RavenPythonLib.mongodb.mongo import Mongo

    # i dont like doing this but its neccessary for recursive database calls
        mongodb = Mongo(isDebug=True, mongoUser=self.args['user'], mongoPath=self.args['dir'],
                        mongoPass="password", mongoIp=self.args['ip'], mongoDbName=self.args['name'],
                        mongoCollName=self.args['coll'], mongoPort=self.args['port'], mongoUrl=self.args['url'],
                        mongoCursorTimeout=self.args['mongoCursorTimeout'])
        return mongodb

    def train(self):
        # this trains the models but autogen must have been called to generate the neural network
        self.modler(toTrain=True)
        self.saveModel()

        # this is what allows continuous training
        if(self.args["epochs"] > self.currentEpoch):
            try:
                self.log(self.prePend + "Epoch: " + str(self.currentEpoch), 0)
                nn = NeuralNetwork(db=self.getNewDatabase(),
                                   logger=self.log,
                                   args=self.args,
                                   model=self.model,
                                   data_pipeline=self.data_pipeline,
                                   currentEpoch=(self.currentEpoch + 1)
                                   )
                cursor = nn.getCursor()
                nn.autogen()
                nn.train()
            except:
                self.log(self.prePend + "could not train dataset: " + str(self.currentEpoch) + "\n" +
                    str(sys.exc_info()[0]) + " " +
                    str(sys.exc_info()[1]), 2)
            finally:
                if(cursor != None) and (cursor.alive):
                    cursor.close()

    def test(self):
        if(self.model):
            self.log(self.prePend +
                     "model already in memory using it for testing", 3)
        else:
            self.log(self.prePend +
                     "model not already in memory attempting retrieval", 3)
            self.getModel()
        if(self.args["testColl"] != ""):

            args = copy.deepcopy(self.args)
            cursor = None
            args["coll"] = args["testColl"]
            args["testColl"] = ""
            try:
                nn = NeuralNetwork(db=self.db,
                                   logger=self.log,
                                   args=args,
                                   model=self.model,
                                   data_pipeline=self.data_pipeline,
                                   model_pipeline=self.model_pipeline,
                                   )
                cursor = nn.getCursor()
                nn.test()

            except:
                print(self.prePend + "could not test on test dataset:\n" +
                    str(sys.exc_info()[0]) + " " +
                      str(sys.exc_info()[1]), 2)
            finally:
                if(cursor != None) and (cursor.alive):
                    cursor.close()
        else:  # TODO seems like this is also called in normal testing but the message suggest recursiveness may want to reword
            self.log(self.prePend + " Recursive neural network call; coll: " +
                     self.args["coll"] + " testColl:" + self.args["testColl"])
            self.modler(toTest=True)
            self.saveResult()

    def predict(self):
        if(self.model):
            self.log(self.prePend +
                     "model already in memory using it for testing", 3)
        else:
            self.log(self.prePend +
                     "model not already in memory attempting retrieval", 3)
            self.getModel()
        self.modler(toPredict=True)

    # the universal interface that allows the code of both test and train to be
    # one single set. "Don't repeat yourself"

    def modler(self, toTrain=False, toTest=False, toPredict=False):
        sumError = 0
        numExamples = 0
        self.numValidExamples = 0

        # check if model exists and that cursor exists
        if(self.model) and (self.cursor):

            if(toTrain == True):
                self.log("training on " + self.args["coll"] + " ...", -1)
            elif(toTest == True):
                self.log("testing on " + self.args["coll"] + " ...", -1)
            elif(toPredict == True):
                self.log("predicting on " + self.args["coll"] + " ...", -1)

            # keep looping while cursor can give more data
            while(self.cursor.alive):
                dataBatch = self.nextDataset(1)
                for mongoDoc in dataBatch:
                    numExamples = numExamples + 1

                    # TODO this is fine if both are pushed lists
                    data = pd.DataFrame(list(mongoDoc["data"]))
                    if(self.args["type"] == "rnn"):
                        data = data.values
                    else:
                        data = np.expand_dims(data.values, axis=0)

                    # TODO needs generalisation for many to many or one to many
                    target = mongoDoc["target"]
                    target = np.full((1, 1), target)

                    if(toTrain == True):
                        self.testTrainer(data=data, target=target,
                                         id=mongoDoc["_id"], toTrain=True)
                    elif(toTest == True):
                        try:
                            sumError = sumError + self.testTrainer(data=data,
                                                                   target=target, id=mongoDoc["_id"], toTrain=False)
                        except TypeError:
                            self.log("NN.testTrainer returned nothing" +
                                str(sys.exc_info()[0]) + " " +
                                str(sys.exc_info()[1]), 3)
                    elif(toPredict == True):
                        self.predictor(
                            data=data, id=mongoDoc["_id"], target=target if target is not None else None)

            if(toTrain == True):
                # cursor is now dead so make it None
                self.cursor = None
                # since this is training we need training accuracy so need to regen cursor
                self.getCursor()
                # call self again but to test now
                self.modler(toTest=True, toTrain=False)
            elif(toTest == True):
                self.sumError = sumError
                self.numExamples = numExamples
                self.modlerStatusMessage()

            elif(toPredict == True):
                None
        else:
            if(toTrain == True):
                self.log(self.prePend +
                         "could not train, either model not generated or cursor does not exist"
                         , 2)

            else:
                self.log(self.prePend +
                         "Aborting test model does not exist; unable to continue"
                         , 2)

    def modlerStatusMessage(self):
        self.log(self.prePend +
                 "\n\tsumError: " + str(self.sumError)
                 + " \n\tnumExamples: " + str(self.numExamples)
                 + " \n\tnumValidExamples " + str(self.numValidExamples)
                 + " \n\tmeanError: "
                 + str(self.sumError / self.numValidExamples),
                 0)

    def testTrainer(self, data, target, id, toTrain=False):
        try:
            if(self.args["type"] == "rnn"):
                target = np.full((self.args["timeSteps"], 1), target)
                expectShape = (self.args["timeSteps"],
                               self.args["dimensionality"])
            else:
                expectShape = (
                    1, self.args["timeSteps"], self.args["dimensionality"])

            # check if shape meets expectations
            if(data.shape == expectShape):

                if(toTrain == True):
                    # self.model.summary()
                    self.model.fit(x=data, y=target, batch_size=self.args["batchSize"],
                                   epochs=self.args["epochs_chunk"], verbose=self.args["kerLogMax"],
                                   callbacks=None, validation_split=0, validation_data=None,
                                   shuffle=True, class_weight=None, sample_weight=None,
                                   initial_epoch=0, steps_per_epoch=None, validation_steps=None)
                else:
                    self.numValidExamples = self.numValidExamples + 1
                    return self.model.evaluate(x=data, y=target,
                                               batch_size=self.args["batchSize"],
                                               verbose=self.args["kerLogMax"])

            else:
                if(self.args["toReduceSpam"] == True):
                    self.log(self.prePend + str(id) + " " + str(data.shape) + " != "
                             + str(expectShape), 3)
                return 0

        except:
            # falling back to args directly just incase is something on the way fked up
            if(self.args["toTrain"]):
                self.log(self.prePend + "could not train:\t" + str(id) + "\n" +
                    str(sys.exc_info()[0]) + " " +
                    str(sys.exc_info()[1]), 2)
            else:
                self.log(self.prePend + "could not test:\t" + str(id) + "\n" +
                    str(sys.exc_info()[0]) + " " +
                    str(sys.exc_info()[1]), 2)

    def predictor(self, data, id, target=None):
        try:
            if(self.args["type"] == "rnn"):
                target = np.full((self.args["timeSteps"], 1), target)
                expectShape = (self.args["timeSteps"],
                               self.args["dimensionality"])
            else:
                expectShape = (
                    1, self.args["timeSteps"], self.args["dimensionality"])

            # check if shape meets expectations
            if(data.shape == expectShape):
                if(target != None):
                    self.log("targ: " + str(target) + " " + str(id), 3)

                x = self.model.predict(x=data, batch_size=self.args["batchSize"],
                                       verbose=self.args["kerLogMax"])
                self.log("pred: " + str(x), 0)

            else:
                self.log(self.prePend + str(id) + " " + str(data.shape) + " != "
                         + str(expectShape), 1)
                return -1

        except:
            self.log(self.prePend + "could not predict:\t" + str(id) + "\n" +
                str(sys.exc_info()[0]) + " " +
                str(sys.exc_info()[1]), 2)

    def saveModel(self):
        if(self.model != None):
            stateDict = self.args

            stateDict["pipe"] = str(self.data_pipeline)
            try:
                del stateDict["pass"]
            except KeyError:
                pass
            stateDict["utc"] = datetime.datetime.utcnow()
            if(self.sumError):
                stateDict["sumError"] = self.sumError
            if(self.numExamples):
                stateDict["numSamples"] = self.numExamples
            if(self.numValidExamples):
                stateDict["numValidSamples"] = self.numValidExamples
            if(self.sumError) and (self.numValidExamples):
                stateDict["meanError"] = self.sumError / self.numValidExamples
            stateDict["currentEpoch"] = self.currentEpoch

            # save model
            self.make_keras_picklable()
            model_bytes = pickle.dumps(self.model)
            stateDict['model_bin'] = Binary(model_bytes)
            self.db.shoveJson(stateDict, collName=str(self.args["modelColl"]))

    def saveResult(self, coll=None):
        if(self.model != None):
            stateDict = self.args
            stateDict["desc"] = "test"
            stateDict["pipe"] = str(self.data_pipeline)
            try:
                del stateDict["pass"]
            except KeyError:
                pass
            stateDict["utc"] = datetime.datetime.utcnow()
            if(self.sumError):
                stateDict["sumError"] = self.sumError
            if(self.numExamples):
                stateDict["numSamples"] = self.numExamples
            if(self.numValidExamples):
                stateDict["numValidSamples"] = self.numValidExamples
            if(self.sumError) and (self.numValidExamples):
                stateDict["meanError"] = self.sumError / self.numValidExamples
            if(self.model_dict != None):
                stateDict["utc"] = datetime.datetime.utcnow()
                stateDict["modelId"] = self.model_dict[0]["_id"]
            self.db.shoveJson(stateDict, collName=str(
                self.args["modelTestColl"]))

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
