# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-22
# @Filename: helpers.py
# @Last modified by:   archer
# @Last modified time: 2019-02-28
# @License: Please see LICENSE file in project root


import argparse
import configparser
import copy
import datetime
import importlib
import json
import os
import subprocess
import sys
import tempfile
import time
import types
from fnmatch import fnmatch

import numpy as np
import pandas as pd
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
        return datetime.datetime.utcfromtimestamp(timeStamp)


# function from http://zachmoshe.com/2017/04/03/pickling-keras-models.html
def make_keras_picklable():
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


def installer(path="./",
              urls=["https://github.com/DreamingRaven/RavenPythonLib"]):

    # neat trick to always ensure path ends in seperator '/' by appending empty
    path = os.path.join(path, "")  # e.g "/usr/bin" vs "/usr/bin/"

    for url in urls:

        if (os.path.exists(path + os.path.basename(url)) == False):
            print(prePend, "find=false installing:",
                  path + os.path.basename(url))
            try:
                os.system("cd " + path + "; git clone " + url)

            except:
                print(prePend,
                      "Could not install:", url, "to",
                      path + os.path.basename(url))


# barebones updater to be used as fallback if full
# featured version is not availiable
def updater(path="./",
            urls=["https://github.com/DreamingRaven/RavenPythonLib"]):

    # neat trick to force filenames to always end in seperator "/"
    path = os.path.join(path, "")  # e.g "/usr/bin" vs "/usr/bin/"

    # attempt self update if permission availiable
    try:
        print(prePend, "Updating self:")
        os.system("cd " + path + "; git pull")

    except:
        print(prePend + "Could not update self")

    for url in urls:
        # update any dependancies
        print(prePend, "Updating", os.path.basename(url) + ":")
        try:
            os.system("cd " + path + os.path.basename(url) + "; git pull")

        except:
            print(prePend + "Could not update dependency: " + url)


def clean(args, print=print):

    print("cleaning: " + str(args["newData"]) + " using: "
          + args["cleaner"] + "...", 3)
    try:
        subprocess.call([
            str(args["cleaner"]),
            "-c", str(args["cleaner"]),
            "--suffix", str(args["suffix"]),
            "--chunkSize", str(args["chunkSize"]),
            "--timeSteps", str(args["timeSteps"]),
            "-d", ] + args["newData"]  # concatenating lists incase more than one file
        )
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

    cursor = None
    try:
        model = None
        for i in range(0, args["epochs"]):
            print("EPOCH: " + str(i), 0)
            nn = NeuralNetwork(db=database,
                               logger=print,
                               args=args,
                               model=model,
                               currentEpoch=i,
                               data_pipeline=getPipeline(
                                   args["pipeline"], print=print)
                               )
            cursor = nn.getCursor()
            nn.autogen()
            model = nn.train()
    except:
        print(prePend + "could not train dataset:\n" +
            str(sys.exc_info()[0]) + " " +
              str(sys.exc_info()[1]), 2)
    finally:
        if(cursor != None) and (cursor.alive):
            cursor.close()


def test(args, database=None, print=print):

    cursor = None
    try:
        nn = NeuralNetwork(db=database,
                           logger=print,
                           args=args,
                           data_pipeline=getPipeline(
                               args["pipeline"], print=print),
                           model_pipeline=getPipeline(
                               args["modelPipe"], print=print),
                           )
        cursor = nn.getCursor()
        nn.test()

    except:
        print(prePend + "could not test dataset:\n" +
            str(sys.exc_info()[0]) + " " +
              str(sys.exc_info()[1]), 2)
    finally:
        if(cursor != None) and (cursor.alive):
            cursor.close()


def predict(args, database=None, print=print):

    cursor = None
    try:
        nn = NeuralNetwork(db=database,
                           logger=print,
                           args=args,
                           data_pipeline=getPipeline(
                               args["pipeline"], print=print),
                           model_pipeline=getPipeline(
                               args["modelPipe"], print=print),
                           )
        cursor = nn.getCursor()
        nn.predict()

    except:
        print(prePend + "could not predict on dataset:\n" +
            str(sys.exc_info()[0]) + " " +
              str(sys.exc_info()[1]), 2)
    finally:
        if(cursor != None) and (cursor.alive):
            cursor.close()


def callCustomScript(args, database=None, print=print):
    try:

        if(os.path.isfile(args["customScript"])):
            None
            # get dir and file strings
            modDir, modFile = os.path.split(args["customScript"])
            # get name from file string is it has an extension for example
            modName = os.path.splitext(modFile)[0]
            # adding location to system path so it can be found
            sys.path.append(modDir)
            print("system path appended with: " + modDir +
                " and successfully found module: " + modFile +
                  " which will now be called")
            argumentz = copy.deepcopy(args)
            del argumentz["pass"]
            # import custom module/ script
            customScript = importlib.import_module(modName)
            # get the entry point function like normal function
            entryPointFunc = getattr(
                customScript, args["customScript_entryPoint"])
            entryPointFunc(args=argumentz, db=database, log=print)

        else:
            # generating error properly without having to try opening it as it
            # is already known to not exist
            open(args["customScript"], "r")

    except FileNotFoundError:
        print(prePend + "(FileNotFoundError)\nlikeley --customScript " +
            args["customScript"] + " does not exist:\n" +
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
