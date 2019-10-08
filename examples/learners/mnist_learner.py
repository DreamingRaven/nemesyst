# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: debug_learner.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root

import keras
import numpy as np


def main(**kwargs):
    # print("kwargs:", type(kwargs), kwargs)

    args = kwargs["args"]
    db = kwargs["db"]

    print(args, args["data_collection"])
    # get a cursor to the data we want (stored internally in db object)
    db.getCursor(db_collection_name=str(args["data_collection"][0]),
                 db_pipeline=[{"$match": {}}])  # using an empty pipeline
    # itetate through the data in batches to minimise requests
    for dataBatch in db.getBatches(db_batch_size=32):
        args["pylog"]("Returned number of documents:", len(dataBatch))

    yield {}
