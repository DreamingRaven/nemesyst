# @Author: George Onoufriou <georgeraven>
# @Date:   2018-05-22
# @Filename: miscHelpers.py
# @Last modified by:   archer
# @Last modified time: 2018-06-04
# @License: Please see LICENSE file in project root



import time
import datetime
import argparse

import types
import tempfile
import os, sys

prePend = "[ " + os.path.basename(sys.argv[0]) + " ] "



def argz(argv=None, description=None):

    if(description == None):
        description = "MongoDb related args"

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-C", "--coll",     default="testColl",
        help="collection name to which data is to be added")
    parser.add_argument("-c", "--clean",    default="",
        help="file list to be cleaned space seperated")
    parser.add_argument("-D", "--dir",      default="~/db/",
        help="directory to store mongodb files/ launch files from")
    parser.add_argument("-I", "--ip",       default="127.0.0.1",
        help="mongod listener, ip address")
    parser.add_argument("-i", "--toInitDb", default=False, action="store_true",
        help="mongod listener, ip address")
    parser.add_argument("-l", "--toLogin",  default=False, action="store_true",
        help="if mongo should log in at end")
    parser.add_argument("-N", "--name",     default="test",
        help="mongo database, name",        required=True)
    parser.add_argument("-P", "--port",     default="27017",
        help="mongod listener, port")
    parser.add_argument("-p", "--pass",     default="i am groot",
        help="mongo user, password",        required=True)
    parser.add_argument("-U", "--url",      default="mongodb://localhost:27017/",
        help="mongod/ destination, url")
    parser.add_argument("-u", "--user",     default="Groot",
        help="mongo user, username",        required=True)
    parser.add_argument("-v", "--loglevel",  default=0, type=int,
        help="verbose output of errors and vals")

    parser.add_argument("--timeSteps",      default=25, type=int,
        help="how many unfolded rnn cells exist and inputs to take")
    parser.add_argument("--testSize",       default=0.2, type=int,
        help="total size * test size = total test set size")
    parser.add_argument("--activation",     default="tanh",
        help="cell activation functions")
    parser.add_argument("--dimensionality", default=19, type=int,
        help="total feature space")
    parser.add_argument("--layers",         default=2, type=int,
        help="how many RNNs should be fully connected")
    parser.add_argument("--lossMetric",     default="mae",
        help="what loss function should be used")
    parser.add_argument("--optimizer",      default="sgd",
        help="what optimizer should be used")
    parser.add_argument("--randomSeed",     default=22, type=int,
        help="set random seed to make results consistent")
    parser.add_argument("--epochs",         default=20, type=int,
        help="set the total number of epochs (repeats) to do")
    parser.add_argument("--intuitivePlots", default=0, type=int,
        help="set the total number intuitive plots to gen")

    return vars(parser.parse_args(argv))



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
