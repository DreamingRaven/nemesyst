# @Author: George Onoufriou <archer>
# @Date:   2019-08-16
# @Email:  george raven community at pm dot me
# @Filename: mnist_learner.py
# @Last modified by:   archer
# @Last modified time: 2019-12-31T17:18:10+00:00
# @License: Please see LICENSE in project root

import numpy as np
import pickle

import keras
from keras import backend as K
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv2D, MaxPooling2D


def main(**kwargs):
    """Entry point called by Nemesyst, always yields dictionary or None.

    :param **kwargs: Generic input method to handle infinite dict-args.
    :rtype: yield dict
    """
    # # there are issues using RTX cards with tensorflow:
    # # https://github.com/tensorflow/tensorflow/issues/24496
    # # if this is the case please uncomment the following two lines:
    import os
    os.environ['CUDA_VISIBLE_DEVICES'] = '-1'  # use cpu

    # just making these a little nicer to read but in a real application
    # we would not want these hardcoded thankfully the database can provide!
    args = kwargs["args"]
    db = kwargs["db"]
    img_rows, img_cols = 28, 28
    num_classes = 10
    # creating two database generators to iterate quickly through the data
    # these are not random they will split data using 60000 as the boundary
    train_generator = inf_mnist_generator(db=db, args=args,
                                          example_dim=(img_rows, img_cols),
                                          num_classes=num_classes,
                                          pipeline=[{"$match":
                                                     {"img_num":
                                                      {"$lt": 60000}}}
                                                    ])
    test_generator = inf_mnist_generator(db=db, args=args,
                                         example_dim=(img_rows, img_cols),
                                         num_classes=num_classes,
                                         pipeline=[{"$match":
                                                    {"img_num":
                                                     {"$gte": 60000}}}
                                                   ])
    # ensuring our input shape is in whatever style keras backend wants
    if K.image_data_format() == 'channels_first':
        input_shape = (1, img_rows, img_cols)
    else:
        input_shape = (img_rows, img_cols, 1)

    model = generate_model(input_shape=input_shape,
                           num_classes=num_classes)
    model.summary()
    hist = model.fit_generator(generator=train_generator,
                               steps_per_epoch=219,  # ceil(70000/32)
                               validation_data=test_generator,
                               validation_steps=219,
                               epochs=args["dl_epochs"][args["process"]],
                               initial_epoch=0)

    excluded_keys = ["pylog", "db_password"]
    # yield metadata, model for gridfs
    best_model = ({
        # metdata dictionary (used to find model later)
        "model": "mnist_example",
        # "validation_loss": float(hist.history["val_loss"][-1]),
        # "validation_accuracy": float(hist.history["val_acc"][-1]),
        "loss": float(hist.history["loss"][-1]),
        "accuracy": float(hist.history["accuracy"][-1]),
        "args": {k: args[k] for k in set(list(args.keys())) - \
                 set(excluded_keys)},
    }, pickle.dumps(model))

    yield best_model


def generate_model(input_shape, num_classes):
    """Generate the keras CNN"""
    model = Sequential()
    model.add(Conv2D(32, kernel_size=(3, 3),
                     activation="relu",
                     input_shape=input_shape))
    model.add(Conv2D(64, (3, 3), activation="relu"))
    model.add(MaxPooling2D(pool_size=(2, 2)))
    model.add(Dropout(0.25))
    model.add(Flatten())
    model.add(Dense(128, activation="relu"))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation="softmax"))

    model.compile(loss=keras.losses.categorical_crossentropy,
                  optimizer=keras.optimizers.Adadelta(),
                  metrics=['accuracy'])
    return model


def inf_mnist_generator(db, args, example_dim, num_classes, pipeline=None):
    """Infinite generator of data for keras fit_generator.

    :param db: Mongo() object to use to fetch data.
    :param args: The user provided args and defaults for adaptation.
    :param example_dim: The tuple dimensions of a single example (row, col).
    :param pipeline: The MongoDB aggregate pipeline [{},{},{}] to use.
    :type db: Mongo
    :type args: dict
    :type example_dim: tuple
    :type num_classes: int
    :type pipeline: list(dict())
    :return: Tuple of a single data batch (x_batch,y_batch).
    :rtype: tuple
    """
    # empty pipeline if none provided
    pipeline = pipeline if pipeline is not None else [{"$match": {}}]
    # loop infiniteley over pipeline
    while True:
        c = db.getCursor(db_collection_name=str(args["data_collection"]
                                                [args["process"]]),
                         db_pipeline=pipeline)
        # itetate through the data in batches to minimise requests
        for data_batch in db.getBatches(db_batch_size=args["dl_batch_size"]
                                        [args["process"]], db_data_cursor=c):
            # we recommend you take a quick read of:
            # https://book.pythontips.com/en/latest/map_filter.html
            y = list(map(lambda d: d["y"], data_batch))
            y = np.array(y)  # converting list to numpy ndarray

            x = list(map(lambda d: d["x"], data_batch))
            x = np.array(x)  # converting nlists to ndarray

            # shaping the np array into whatever keras is asking for
            if K.image_data_format() == 'channels_first':
                y = y.reshape((y.shape[0], 1))
                x = x.reshape((x.shape[0], 1,
                               example_dim[0], example_dim[1]))
                # input_shape = (1, example_dim[0], example_dim[1])
            else:
                y = y.reshape((y.shape[0], 1))
                x = x.reshape((x.shape[0],
                               example_dim[0], example_dim[1], 1))
                # input_shape = (example_dim[0], example_dim[1], 1)

            # normalising to 0-1
            x = x.astype('float32')
            x /= 255

            # convert class vectors to binary class matrices
            y = keras.utils.to_categorical(y, num_classes)

            # returning completeley propper data, batch by batch thats all.
            yield x, y
