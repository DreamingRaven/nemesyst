# @Author: George Onoufriou <georgeraven>
# @Date:   2018-12-11
# @Filename: data.py
# @Last modified by:   georgeraven
# @Last modified time: 2018-12-11
# @License: Please see LICENSE in project root.
# @Copyright: George Onoufriou

import os
import sys
from collections.abc import MutableMapping


class Data():

    def __init__(self, args, db, log):
        self.args = args
        self.db = db
        self.log = log
