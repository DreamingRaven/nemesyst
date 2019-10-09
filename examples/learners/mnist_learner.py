# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: mnist_learner.py
# @Last modified by:   archer
# @Last modified time: 2019-10-09
# @License: Please see LICENSE in project root

import keras
import numpy as np


def main(**kwargs):
    # just making these a little nicer to use
    args = kwargs["args"]
    db = kwargs["db"]
    # get a cursor to the data we want (stored internally in db object)
    db.getCursor(db_collection_name=str(args["data_collection"][0]),
                 db_pipeline=[{"$match": {}}])  # using an empty pipeline
    # itetate through the data in batches to minimise requests
    for dataBatch in db.getBatches(db_batch_size=args["dl_batch_size"]
                                   [args["process"]]):
        # we recommend you take a quick read of:
        # https://book.pythontips.com/en/latest/map_filter.html
        y = list(map(lambda d: d["y"], dataBatch))
        y = np.array(y)  # converting list to numpy ndarray
        x = list(map(lambda d: d["x"], dataBatch))
        x = np.array(x)  # converting list of lists to numpy ndarray
    args["pylog"](x, y)
    args["pylog"](x.shape, y.shape)
    yield {}
