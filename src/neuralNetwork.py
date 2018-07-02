# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: NeuralNetwork.py
# @Last modified by:   archer
# @Last modified time: 2018-07-02
# @License: Please see LICENSE file in project root



import pickle
import os, sys
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM



class NeuralNetwork():



    home = os.path.expanduser("~")
    fileName = "neuralNetwork"
    prePend = "[ " + fileName + "] "



    def __init__(self, logger=print):
        self.log = logger
        None
        # raise NotImplementedError('NN.__init__() not currentley implemented')



    def debug(self):
        None



    def autogen(self):
        None
        self.make_keras_picklable()
        self.log(self.prePend + "hells yes", 3)
        raise NotImplementedError('NN.autogen() not currentley implemented')



    def compile(self):
        None
        raise NotImplementedError('NN.compile() not currentley implemented')



    def loadModel():
        None



    def saveModel():
        None



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
