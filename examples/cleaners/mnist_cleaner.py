# @Author: George Onoufriou <archer>
# @Date:   2019-08-15
# @Email:  george raven community at pm dot me
# @Filename: debug_cleaner.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root
import io
import datetime
from sklearn.datasets import fetch_openml


def main(**kwargs):
    print("downloading mnist dataset...")
    x, y = fetch_openml('mnist_784', version=1, return_X_y=True)
    utc_import_start_time = datetime.datetime.utcnow()
    print("importing mnist dataset to mongodb...")
    # TODO: vectorize on outermost dimension (rowise not elementwise)
    for i in range(len(x)):
        document = {
            "x": x[i].tolist(),     # converting to list to be bson compatible
            "y": y[i],              # keeping as num could also be list
            "img_num": i,           # saving the image number
            "utc_import_time":  utc_import_start_time,
            "dataset": "mnist"
        }
        yield document
