# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-22
# @Filename: helpers.py
# @Last modified by:   archer
# @Last modified time: 2018-07-12
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



# the super argument handler prioritizing command line falling back to config file
def argz(argv=None, description=None, prevArgs=None):

    # declaring outside scope to make it clear what scope it is destined for
    config = None
    options = "options"
    # importing config file after the config file location is known in prevArgs
    if(prevArgs != None):
        config = configparser.ConfigParser()
        # configFiles_paths = [str(rootPath + "/config/rrs_ml.ini", prevArgs["config"]]
        config.read(prevArgs["config"])

    if(description == None):
        description = "MongoDb related args"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-C", "--coll",
        default=str( argDeflt(config, options, "coll", "testColl") ),
        help="collection name to which data is to be added")
    parser.add_argument("-c", "--cleaner",
        default=str( argDeflt(config, options, "cleaner", "" ) ),
        help="file inclusive path to cleaner file, for data specific cleaning, should also specify --newData")
    parser.add_argument("-D", "--dir",
        default=str( argDeflt( config, options, "dir", str(home + "/db"))),
        help="directory to store mongodb files/ launch files from")
    parser.add_argument("-d", "--newData",
        default=str( argDeflt( config, options, "newData", str("")) ),
        help="the directory or file of the new data to be added and cleaned, should also specify --cleaner")
    parser.add_argument("-I", "--ip",
        default="127.0.0.1",
        help="mongod listener, ip address")
    parser.add_argument("-i", "--toInitDb",
        default=False, action="store_true",
        help="flag to initialise database with user")
    parser.add_argument("-l", "--toLogin",
        default=False, action="store_true",
        help="if mongo should log in at end")
    parser.add_argument("-N", "--name",
        default="RecSyst",
        help="mongo database, name",        required=True)
    parser.add_argument("-P", "--port",
        default="27017",
        help="mongod listener, port")
    parser.add_argument("-p", "--pass",
        default="i am groot",
        help="mongo user, password",        required=True)
    parser.add_argument("-S", "--toStartDb",
        default=False, action="store_true",
        help="flag to start database, this starts in authentication only mode")
    parser.add_argument("-s", "--toStopDb",
        default=False, action="store_true",
        help="flag to stop database, this is the least priority action")
    parser.add_argument("-T", "--toTrain",
        default=False, action="store_true",
        help="flag to train on availiable dataset")
    parser.add_argument("-t", "--toTest",
        default=False, action="store_true",
        help="flag to test on availiable dataset")
    parser.add_argument("-U", "--url",
        default="mongodb://localhost:27017/",
        help="mongod/ destination, url")
    parser.add_argument("-u", "--user",
        default="Groot",
        help="mongo user, username",        required=True)
    parser.add_argument("-v", "--loglevel",
        default=0,      type=int,
        help="verbose output of errors and vals")

    parser.add_argument("--timeSteps",      default=25,     type=int,
        help="how many unfolded rnn cells exist and inputs to take")
    parser.add_argument("--testSize",       default=0.2,    type=int,
        help="total size * test size = total test set size")
    parser.add_argument("--activation",     default="tanh",
        help="cell activation functions")
    parser.add_argument("--dimensionality", default=19,     type=int,
        help="total feature space")
    parser.add_argument("--layers",         default=2,      type=int,
        help="how many RNNs should be fully connected")
    parser.add_argument("--lossMetric",     default="mae",
        help="what loss function should be used")
    parser.add_argument("--optimizer",      default="sgd",
        help="what optimizer should be used")
    parser.add_argument("--randomSeed",     default=22,     type=int,
        help="set random seed to make results consistent")
    parser.add_argument("--epochs",         default=20,     type=int,
        help="set the total number of epochs (repeats) to do")
    parser.add_argument("--suffix",         default=".data",
        help="set the suffix to append to generated clean data files")
    parser.add_argument("--chunkSize",      default=10**8,  type=int,
        help="sets the size in rows of csv to be read in as chunks")
    parser.add_argument("--toJustImport",   default=False, action="store_true",
        help="sets flag to just import without cleaning")
    parser.add_argument("--pipeline",         default=str(rootPath + "/config/rrs_pipeline.json"),
        help="set the path to the json pipeline file")
    parser.add_argument("--config",         default=str(rootPath + "/config/rrs_ml.ini"),
        help="set the main config file for ravenRecSyst using absolute path")

    args = vars(parser.parse_args(argv))

    # identifying arguments by name which are paths to be normalised
    pathArgNames = ["cleaner", "dir", "newData"]
    normalArgs = normaliseArgs(args=args, pathArgNames=pathArgNames)

    # importing json pipeline config file after the args are in their final form
    if(prevArgs != None):
        try:
            #TODO: add an arg for this
            with open(normalArgs["pipeline"], 'r') as f:
                pipeline = json.load(f)
        except:
            print(prePend + "could not load a .json config file:\n" +
            str(sys.exc_info()[0]) + " " +
            str(sys.exc_info()[1]) , 1)

    # run again if args do not include config files I.E they have no previous state
    if(prevArgs != None):
        return normalArgs
    else:
        return argz(argv=argv, description=description, prevArgs=normalArgs)



def normaliseArgs(args, pathArgNames):

    # normalizing args identified in list
    for argName in pathArgNames:
        args[argName] = str(os.path.abspath(args[argName]))

    return args



def argDeflt(conf, section, key, fallbackVal):

    #TODO: this is very awkward because it might be called where conf is None
    try:
        val = conf[str(section)][str(key)]


        if(val == ""):
            print(key, "=", fallbackVal, ";\t", bool(val), type(val))
            return fallbackVal
        else:
            print(key, "=", val, ";\t", bool(val), type(val))
            return val

    except:
        return fallbackVal



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



def train(args, database=None, print=print):

    try:
        nn = NeuralNetwork(db=database, logger=print)
        nn.debug()
        nn.autogen()
        raise NotImplementedError('data training not currentley implemented')

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
    from sys import argv

    args = argz(argv[1:]) # get all command line args
    print(args['ip'])

    ts = getTimestamp()
    dt1 = getDateTime()
    dt2 = getDateTime(ts)
    ts1 = getTimestamp(dt1)
    ts2 = getTimestamp(dt2)

    print("Timestamps should match as should datetimes:",
          "\nts =", ts, "\t\t\tgenerated timestamp",
          "\ndt1 =", dt1, "\tgenerated datetime",
          "\ndt2 =", dt2, "\tconverted from generated timestamp (ts)",
          "\nts1 =", ts1, "\t\t\tconverted from generated datetime (dt1)",
          "\nts2 =", ts2, "\t\t\tconverted from generated datetime (dt2)"
          )
