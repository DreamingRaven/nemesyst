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

    # args["pylog"](x.reshape(x.shape[0], 28, 28, 1).shape())

    # testing keras inbuilt method
    from keras.datasets import mnist
    from keras.models import Sequential
    from keras.layers import Dense, Dropout, Flatten
    from keras.layers import Conv2D, MaxPooling2D
    from keras import backend as K

    batch_size = 128
    num_classes = 10
    epochs = 12

    # input image dimensions
    img_rows, img_cols = 28, 28

    # the data, split between train and test sets
    (x_train, y_train), (x_test, y_test) = mnist.load_data()

    if K.image_data_format() == 'channels_first':
        x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
        x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
        input_shape = (1, img_rows, img_cols)
    else:
        x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
        x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
        input_shape = (img_rows, img_cols, 1)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')

    yield {}
