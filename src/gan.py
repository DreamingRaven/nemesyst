#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-07-02
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-08-28
# @License: Please see LICENSE file in project root



# import pickle
import os, sys, pprint
import pandas as pd
import numpy as np
# import datetime
# from bson import objectid, Binary
from keras.models import Sequential
from keras.layers import Dense, Activation, LSTM



class Gan():



    home = os.path.expanduser("~")
    fileName = "gan"
    prePend = "[ " + fileName + " ] "



    def __init__(self, args, logger=print):
        m_args = args
        self.log  = logger if logger is not None else print

        try:
            del m_args["pass"]
        except:
            self.log("Could not delete password entry, make sure args exists")

        self.args = m_args
        self.generator  = None
        self.discriminator = None



    def debug(self):
        None
        pprint.pprint(self.args)
        # self.log(self.prePend                                   + "\n"  +
        #          "\tdb obj: " + str(self.db)                    + "\n"  +
        #          "\tdb pipeline: " + str(self.data_pipeline)    + "\n"  +
        #          "\tdb cursor: " + str(self.cursor)             + "\n"  +
        #          "\tlogger: " + str(self.log)                   ,
        #          0)



    def genGenerator(self):
        None



    def genDiscriminator(self):
        None
