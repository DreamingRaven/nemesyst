#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: NeuralNetwork.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-07-15
# @License: Please see LICENSE file in project root



import pickle
import os, sys
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM

# link for getting distinct values in collection for test train splitting
# http://api.mongodb.com/python/1.4/api/pymongo/collection.html#pymongo.collection.Collection.distinct

class NeuralNetwork():



    home = os.path.expanduser("~")
    fileName = "neuralNetwork"
    prePend = "[ " + fileName + " ] "



    def __init__(self, db, logger=print):
        self.log = logger
        self.db = db
        self.log(self.prePend + "NN.init() success", 3)



    def debug(self):
        self.log(self.prePend       + "\n"  +
                 "\tdb obj: " + str(self.db)  + "\n"  +
                 "\tlogger: " + str(self.log),
                 0)



    def autogen(self):
        None
        self.make_keras_picklable()
        raise NotImplementedError('NN.autogen() not currentley implemented')



    def compile(self):
        None
        raise NotImplementedError('NN.compile() not currentley implemented')



    def loadModel():
        None
        raise NotImplementedError('NN.loadModel() not currentley implemented')



    def saveModel():
        None
        raise NotImplementedError('NN.saveModel() not currentley implemented')



    def train():
        None
        raise NotImplementedError('NN.tain() not currentley implemented')



    def test():
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
