# @Author: George Onoufriou <archer>
# @Date:   2019-08-15
# @Email:  george raven community at pm dot me
# @Filename: debug_cleaner.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16T15:04:11+01:00
# @License: Please see LICENSE in project root


def main(**kwargs):
    print("kwargs:", type(kwargs), kwargs)
    x = 0
    while x < 10:
        yield {"x": x}
        x = x + 1
