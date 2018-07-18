# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-22
# @Filename: helpers.py
# @Last modified by:   archer
# @Last modified time: 2018-07-18
# @License: Please see LICENSE file in project root



import os, sys, subprocess, tempfile, types, json, \
       argparse, datetime, time, configparser
import pandas as pd
import numpy as np
from fnmatch import fnmatch
from src.neuralNetwork import NeuralNetwork



fileName = "helpers.py"
prePend = "[ " + fileName + " ] "
home = os.path.expanduser("~")
rootPath, _ = os.path.split(os.path.abspath(sys.argv[0]))



# either generates timestamp UTC or converts existing datetime
def getTimestamp(dateTime=None):

    if (dateTime == None):
        return int(time.time())
    else:
        return int(dateTime.replace(tzinfo=datetime.timezone.utc).timestamp())



# either generates datetime UTC or converts existing timestamp
def getDateTime(timeStamp=None):

    if(timeStamp == None):
        timeStamp = int(time.time())
        return datetime.datetime.utcfromtimestamp(timeStamp)
    else:
        return datetime.datetime.utcfromtimestamp(timeStamp)#.strftime('%Y-%m-%d %H:%M:%S') # converts to string



# function from http://zachmoshe.com/2017/04/03/pickling-keras-models.html
def make_keras_picklable():
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



def installer(path="./",
              urls=["https://github.com/DreamingRaven/RavenPythonLib"]):

    # neat trick to always ensure path ends in seperator '/' by appending empty
    path = os.path.join(path, "") # e.g "/usr/bin" vs "/usr/bin/"

    for url in urls:

        if (os.path.exists(path + os.path.basename(url)) == False):
            print(prePend, "find=false installing:",
                path + os.path.basename(url))
            try:
                os.system("cd " + path + "; git clone " + url)

            except:
                print(prePend,
                    "Could not install:", url , "to",
                    path + os.path.basename(url) )



# barebones updater to be used as fallback if full
# featured version is not availiable
def updater(path="./",
            urls=["https://github.com/DreamingRaven/RavenPythonLib"]):

    # neat trick to force filenames to always end in seperator "/"
    path = os.path.join(path, "") # e.g "/usr/bin" vs "/usr/bin/"

    # attempt self update if permission availiable
    try:
        print(prePend, "Updating self:")
        os.system("cd " + path + "; git pull")

    except:
        print(prePend + "Could not update self")

    for url in urls:
        # update any dependancies
        print(prePend, "Updating", os.path.basename(url) + ":" )
        try:
            os.system("cd " + path + os.path.basename(url) + "; git pull")

        except:
            print(prePend + "Could not update dependency: " + url)



def clean(args, print=print):

    print("cleaning: " + args["newData"] + " using: "
            + args["cleaner"] + "...", 3)
    try:
        subprocess.call([
            str(args["cleaner"]),
            "-d"                , str(args["newData"]),
            "-c"                , str(args["cleaner"]),
            "--suffix"           , str(args["suffix"]),
            "--chunkSize"       , str(args["chunkSize"]),
            "--timeSteps"       , str(args["timeSteps"]),
            ])
        print("cleaner returned", 3)

    except:
        print(prePend + "could not clean dataset:\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]), 2)



def getPipeline(pipePath, print=print):
    try:
        with open(pipePath) as f:
            return json.load(f)
    except:
        print(prePend + "could not get pipeline from: " + str(pipePath) + "\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]), 2)



def train(args, database=None, print=print):

    try:
        nn = NeuralNetwork(db=database,
                           logger=print,
                           args=args,
                           pipeline=getPipeline(args["pipeline"], print=print)
                          )
        nn.debug()
        nn.getCursor()
        nn.autogen()

    except:
        print(prePend + "could not train dataset:\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]), 2)



def test(args, print=print):

    try:
        raise NotImplementedError('data testing not currentley implemented')

    except:
        print(prePend + "could not test dataset:\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]), 2)



def predict(args, print=print):

    try:
        raise NotImplementedError('data predicting not currentley implemented')

    except:
        print(prePend + "could not predict on dataset:\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]), 2)



def getDirPath(path):
    folderPath, file = os.path.split(path)
    return folderPath


def getFileName(path):
    folderPath, file = os.path.split(path)
    return file


if __name__ == "__main__":
    None
