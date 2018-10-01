#!/usr/bin/env python3

# @Author: George Onoufriou <archer>
# @Date:   2018-09-27
# @Filename: gan.py
# @Last modified by:   archer
# @Last modified time: 2018-10-01
# @License: Please see LICENSE file in project root

import sys
# this is calling system wide nemesyst src.arg so if you are working on a branch
# dont forget this will be the main branch version of args
from src.arg import argz
description="Nemesyst template file"
args = argz(sys.argv[1:], description=description)

print(sys.path)

def main(args, db, log):
    print(args)
    print("hi there")
