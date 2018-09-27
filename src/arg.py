# @Author: George Onoufriou <archer>
# @Date:   2018-07-18
# @Filename: arg.py
# @Last modified by:   archer
# @Last modified time: 2018-09-27
# @License: Please see LICENSE file in project root

import os, sys, types, json, \
       argparse, configparser, getpass
from fnmatch import fnmatch



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
        config.read(prevArgs["config"])
    else:
        # this allows for the default config to be read first then redirected
        # to the overidden one
        config = configparser.ConfigParser()
        config.read(str(rootPath + "/config/config.ini"))

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
        default=str( argDeflt(config, options, "ip", str("127.0.0.1")) ),
        help="mongod listener, ip address")
    parser.add_argument("-i", "--toInitDb",
        default=bool( argDeflt( config, options, "toInitDb", False, isBool=True) ),
        action="store_true",
        help="flag to initialise database with user")
    parser.add_argument("-l", "--toLogin",
        default=bool( argDeflt( config, options, "toLogin", False, isBool=True) ),
        action="store_true",
        help="if mongo should log in at end")
    parser.add_argument("-N", "--name",
        default=str( argDeflt( config, options, "name", str("RecSyst")) ),
        help="mongo database, name",
        required=False)
    parser.add_argument("-P", "--port",
        default=str( argDeflt( config, options, "port", str("27017")) ),
        help="mongod listener, port")
    parser.add_argument("-p", "--pass",
        default=str( argDeflt( config, options, "pass", str("iamgroot")) ),
        help="mongo user, password",
        required=False)
    parser.add_argument("-S", "--toStartDb",
        default=bool( argDeflt( config, options, "toStartDb", False, isBool=True) ),
        action="store_true",
        help="flag to start database, this starts in authentication only mode")
    parser.add_argument("-s", "--toStopDb",
        default=bool( argDeflt( config, options, "toStopDb", False, isBool=True) ),
        action="store_true",
        help="flag to stop database, this is the least priority action")
    parser.add_argument("-T", "--toTrain",
        default=bool( argDeflt( config, options, "toTrain", False, isBool=True) ),
        action="store_true",
        help="flag to train on availiable dataset")
    parser.add_argument("-t", "--toTest",
        default=bool( argDeflt( config, options, "toTest", False, isBool=True) ),
        action="store_true",
        help="flag to test on availiable dataset")
    parser.add_argument("-U", "--url",
        default=str( argDeflt( config, options, "url", str("mongodb://localhost:27017/")) ),
        help="mongod/ destination, url")
    parser.add_argument("-u", "--user",
        default=str( argDeflt( config, options, "user", str("groot")) ),
        help="mongo user, username",
        required=False)
    parser.add_argument("-v", "--loglevel",
        default=int( argDeflt( config, options, "loglevel", int(0)) ),
        type=int,
        help="verbose output of errors and vals")

    parser.add_argument("--batchSize",
        default=int( argDeflt( config, options, "batchSize", int(1)) ),
        type=int,
        help="sets the batchsize to be used, i.e how many samples before the model weights are updated")
    parser.add_argument("--target",
        default=str( argDeflt( config, options, "target", str("target")) ),
        help="what loss function should be used")
    parser.add_argument("--type",
        default=str( argDeflt( config, options, "type", str("lstm")) ),
        help="what loss function should be used")
    parser.add_argument("--timeSteps",
        default=int( argDeflt( config, options, "timeSteps", int(25)) ),
        type=int,
        help="how many unfolded rnn cells exist and inputs to expect to take")
    parser.add_argument("--testSize",
        default=float( argDeflt( config, options, "testSize", float(0.2)) ),
        type=float,
        help="total size * test size = total test set size")
    parser.add_argument("--activation",
        default=str( argDeflt( config, options, "activation", str("tanh")) ),
        help="cell activation functions from keras")
    parser.add_argument("--dimensionality", # is this even neccessary?
        default=int( argDeflt( config, options, "dimensionality", int(19)) ),
        type=int,
        help="total feature space")
    parser.add_argument("--layers",
        default=int( argDeflt( config, options, "layers", int(2)) ),
        type=int,
        help="how many RNNs should be fully connected")
    parser.add_argument("--lossMetric",
        default=str( argDeflt( config, options, "lossMetric", str("mae")) ),
        help="what loss function should be used")
    parser.add_argument("--optimizer",
        default=str( argDeflt( config, options, "optimizer", str("sgd")) ),
        help="what optimizer should be used")
    parser.add_argument("--randomSeed",
        default=int( argDeflt( config, options, "randomSeed", int(22)) ),
        type=int,
        help="set random seed to make results consistent")
    parser.add_argument("--epochs",
        default=int( argDeflt( config, options, "epochs", int(20)) ),
        type=int,
        help="set the total number of epochs (repeats) to do")
    parser.add_argument("--suffix",
        default=str( argDeflt( config, options, "suffix", str(".data")) ),
        help="set the suffix to append to generated clean data files")
    parser.add_argument("--chunkSize",
        default=int( argDeflt( config, options, "chunkSize", int(10**8)) ),
        type=int,
        help="sets the size in rows of csv to be read in as chunks")
    parser.add_argument("--toJustImport",
        default=bool( argDeflt( config, options, "toJustImport", False, isBool=True) ),
        action="store_true",
        help="sets flag to just import without cleaning")
    parser.add_argument("--pipeline",
        default=str( argDeflt( config, options, "pipeline", str(rootPath + "/config/pipeline.json")) ),
        help="set the path to the json pipeline file")
    parser.add_argument("--config",
        default=str( argDeflt( config, options, "config", str(rootPath + "/config/config.ini")) ),
        help="set the main config file for ravenRecSyst using absolute path")
    parser.add_argument("--mongoCursorTimeout",
        default=int( argDeflt( config, options, "mongoCursorTimeout", int(600000)) ),
        type=int,
        help="set the time in milliseconds for cursors to timeout")
    parser.add_argument("--kerLogMax",
        default=int( argDeflt( config, options, "kerLogMax", int(0)) ),
        type=int,
        help="set the max log level for keras to log")
    parser.add_argument("--toUpdate",
        default=bool( argDeflt( config, options, "toUpdate", False, isBool=True) ),
        action="store_true",
        help="sets flag to automate updating and for first time installation")
    parser.add_argument("--modelColl",
        default=str( argDeflt( config, options, "modelColl", str("models")) ),
        help="set the collection to which state will be tracked and model binary kept")
    parser.add_argument("--identifier",
        default=str( argDeflt( config, options, "identifier", str(getpass.getuser())) ),
        help="set an identifier for collections to be able to filter models serves no direct purpose")
    parser.add_argument("--tfLogMin",
        default=int( argDeflt( config, options, "tfLogMin", int(1)) ),
        type=int,
        help="set the minimum log level for tensorflow, i.e TF_CPP_MIN_LOG_LEVEL")
    parser.add_argument("--toPredict",
        default=bool( argDeflt( config, options, "toPredict", False, isBool=True) ),
        action="store_true",
        help="sets flag to predict based on data in a collection")
    parser.add_argument("--modelPipe",
        default=str( argDeflt( config, options, "modelPipe", str(rootPath + "/config/modelPipe.json")) ),
        help="set the path to the json pipeline file")
    parser.add_argument("--intLayerDim",
        default=int( argDeflt( config, options, "intLayerDim", int(200)) ),
        type=int,
        help="set the dimensionality between layers")
    parser.add_argument("--epochs_chunk",
        default=int( argDeflt( config, options, "epochs_chunk", int(1)) ),
        type=int,
        help="set the number of epochs each chunk will iterate, this is different to --epochs since that iterates over all the data instead")
    parser.add_argument("--toRetrain",
        default=bool( argDeflt( config, options, "toRetrain", False, isBool=True) ),
        action="store_true",
        help="sets flag to continue training a model provided by the model pipeline")
    parser.add_argument("--nnScript",
        default=str( argDeflt( config, options, "nnScript", str(rootPath + "/examples/gan.py")) ),
        help="set the path to the json pipeline file")





    args = vars(parser.parse_args(argv))

    # identifying arguments by name which are paths to be normalised
    pathArgNames = ["cleaner", "dir", "newData", "pipeline", "modelPipe", "nnScript"]
    normalArgs = normaliseArgs(args=args, argNames=pathArgNames)
    # identifying arguments that are single words that want to be normalised
    wantedInLowerCase = ["type", "activation", "lossMetric", "optimizer"]
    normalArgs = normaliseArgs(args=args, argNames=wantedInLowerCase, toMakeLowerCase=True)

    # run again if args do not include config files I.E they have no previous state
    if(prevArgs != None):
        return normalArgs
    else:
        return argz(argv=argv, description=description, prevArgs=normalArgs)



def normaliseArgs(args, argNames, toMakeLowerCase=False):

    # normalizing args identified in list
    for argName in argNames:
        # this normalises the case of text to lower case
        if(toMakeLowerCase == True):
            args[argName] = args[argName].casefold()
        # this if statement prevents abspath from interpreting "" as current dir
        elif(args[argName] != ""):
            args[argName] = str(os.path.abspath(args[argName]))

    return args



def argDeflt(conf, section, key, fallbackVal, isBool=False):

    #TODO: this is very awkward because it might be called where conf is None
    try:
        val = ""
        if(isBool == False):
            val = conf[str(section)][str(key)]
        else:
            val = conf.getboolean(str(section), str(key))

        if(val == ""):
            # print(key, "=\t", fallbackVal, ";\t", bool(fallbackVal), type(val))
            return fallbackVal
        else:
            # print(key, "=\t", val, ";\t", bool(val), type(val))
            return val

    except:
        return fallbackVal
