# @Author: George Onoufriou <archer>
# @Date:   2018-11-08
# @Filename: argZ.py
# @Last modified by:   archer
# @Last modified time: 2018-11-08
# @License: Please see LICENSE file in project root

import os, sys
from collections.abc import MutableMapping # abstract base classes (abc)



# abstract dict = ADict, has all main dict functions + key safe + expandable
class ADict(MutableMapping):



    def __init__(self, dictz=None):
        self.dict = dictz if dictz is not None else dict()



    def __getitem__(self, key):
        try:
            return self.dict[key]
        except KeyError:
            pass # what was asked does not exist which is the same as None so will not error
        except TypeError:
            print("TypeError: cannot use:", key, "with object:", type(self.dict))



    def __setitem__(self, key, value):
        self.dict[key] = value



    def __delitem__(self, key):
        try:
            del self.dict[key]
        except KeyError:
            pass # job is not done but equivelant outcomes so will not error



    def __iter__(self):
        return iter(self.dict)



    def __len__(self):
        return len(self.dict)



    def swapDict(self, newDict):
        oldDict = self.dict
        self.dict = newDict
        return oldDict



# tests on overloaded functions to check functionality is correct!
if(__name__ == "__main__"):

    dictz = {
        "notFlower": "teaspoon",
        "chief": 117,
        "dingDong": "theWitchIsDead",
    }
    dictz2 = {
        "flower": "buttercup",
        "jimmy": 69,
        "my name is phil": "nice to meet you phil",
    }

    # check init
    duct = DictUtil(dictz=dictz)
    # check changing dict is possible
    oldDict = duct.swapDict(dictz2)
    # check getting value is possible
    value = duct["flower"]
    # check setting value is possible
    duct["flower"] = 64
    # check dleting key is possible (but depend on dict swap working)
    del duct["flower"]
    # check dict is iteratable
    for key in duct:
        str(key + " : " + str(duct[key]) + " " + str(len(duct)))
    # check dict does not throw error if key is missued and returns None
    didError = duct["jimmyridler"]
