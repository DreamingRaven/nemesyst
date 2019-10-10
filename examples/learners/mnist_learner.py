# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: mnist_learner.py
# @Last modified by:   archer
# @Last modified time: 2019-10-09T14:35:50+01:00
# @License: Please see LICENSE in project root

import numpy as np
import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


def main(**kwargs):
    # just making these a little nicer to use
    args = kwargs["args"]
    db = kwargs["db"]
    img_rows, img_cols = 28, 28
    num_classes = 10
    model = None

    for epoch in range(args["dl_epochs"][args["process"]]):
        # get a cursor to the data we want (stored internally in db object)
        args["pylog"]("Epoch:", epoch)
        db.getCursor(db_collection_name=str(args["data_collection"]
                                            [args["process"]]),
                     db_pipeline=[{"$match": {}}])  # using an empty pipeline

        # itetate through the data in batches to minimise requests
        for data_batch in db.getBatches(db_batch_size=args["dl_batch_size"]
                                        [args["process"]]):
            # we recommend you take a quick read of:
            # https://book.pythontips.com/en/latest/map_filter.html
            y_train = list(map(lambda d: d["y"], data_batch))
            y_train = np.array(y_train)  # converting list to numpy ndarray

            x_train = list(map(lambda d: d["x"], data_batch))
            x_train = np.array(x_train)  # converting nlists to ndarray

            if K.image_data_format() == 'channels_first':
                y_train = y_train.reshape((y_train.shape[0], 1))
                x_train = x_train.reshape((x_train.shape[0], 1,
                                           img_rows, img_cols))
                input_shape = (1, img_rows, img_cols)
            else:
                y_train = y_train.reshape((y_train.shape[0], 1))
                x_train = x_train.reshape((x_train.shape[0],
                                           img_rows, img_cols, 1))
                input_shape = (img_rows, img_cols, 1)

            data_ids = list(map(lambda d: d["_id"], data_batch))

            x_train = x_train.astype('float32')
            x_train /= 255

            # convert class vectors to binary class matrices
            y_train = keras.utils.to_categorical(y_train, num_classes)

            # ensuring model is not recreated every time
            if model is None:
                model = Sequential()
                model.add(Conv2D(32, kernel_size=(3, 3),
                                 activation='relu',
                                 input_shape=input_shape))
                model.add(Conv2D(64, (3, 3), activation='relu'))
                model.add(MaxPooling2D(pool_size=(2, 2)))
                model.add(Dropout(0.25))
                model.add(Flatten())
                model.add(Dense(128, activation='relu'))
                model.add(Dropout(0.5))
                model.add(Dense(num_classes, activation='softmax'))

                model.compile(loss=keras.losses.categorical_crossentropy,
                              optimizer=keras.optimizers.Adadelta(),
                              metrics=['accuracy'])

            if(x_train.shape == (args["dl_batch_size"], 1,
                                 img_rows, img_cols))\
                    or (x_train.shape == (args["dl_batch_size"],
                                          img_rows, img_cols, 1)):
                model.fit(x_train, y_train,
                          batch_size=args["dl_batch_size"][args["process"]],
                          epochs=1,  # args["dl_epochs"][args["process"]],
                          # verbose=1,
                          # validation_data=(x_test, y_test)
                          )

    yield {}
