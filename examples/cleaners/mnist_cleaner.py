# @Author: George Onoufriou <archer>
# @Date:   2019-08-15
# @Email:  george raven community at pm dot me
# @Filename: debug_cleaner.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root
import io
from sklearn.datasets import fetch_openml


def main(**kwargs):
    print("kwargs:", type(kwargs), kwargs)
    print("downloading mnist dataset...")

    x, y = fetch_openml('mnist_784', version=1, return_X_y=True)

    X = 0
    while X < 10:
        yield {"x": X}
        X = X + 1
