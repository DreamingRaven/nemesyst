#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-10-01
# @License: Please see LICENSE file in project root

import sys

fileName = "gan.py"
prePend = "[ " + fileName + " ] "
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args

def main(args, db, log):

    log( prePend + "\n\tArg dict of length: " + str(len(args)) +
        "\n\tDatabase obj: " + str(db) + "\n\tLogger object: " + str(log), 0)
    print("hellow-orld")
