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


class Data(MutableMapping):

    def __init__(self, args, db, log):
        self.args = args
        self.db = db
        self.log = log

    def __delitem__(self):
        raise NotImplementedError("Data.__delitem__() is not yet implemented")

    def __getitem__(self):
        raise NotImplementedError("Data.__getitem__() is not yet implemented")

    def __iter__(self):
        raise NotImplementedError("Data.__iter__() is not yet implemented")

    def __len__(self):
        raise NotImplementedError("Data.__len__() is not yet implemented")

    def __setitem__(self):
        raise NotImplementedError("Data.__setitem__() is not yet implemented")
