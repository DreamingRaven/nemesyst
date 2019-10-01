# @Author: George Onoufriou <archer>
# @Date:   2019-08-15
# @Email:  george raven community at pm dot me
# @Filename: debug_cleaner.py
# @Last modified by:   archer
# @Last modified time: 2019-08-16
# @License: Please see LICENSE in project root
import urllib.request
import gzip
import io


def download(url):
    # https://stackoverflow.com/a/34109395
    r = urllib.request.urlopen(url)
    return r


def main(**kwargs):
    print("kwargs:", type(kwargs), kwargs)

    print("downloading mnist dataset...")

    r = download('http://yann.lecun.com/exdb/mnist/train-images-idx3-ubyte.gz')

    print(r)
    compressed_file = io.BytesIO(r.read())
    decompressed_file = gzip.GzipFile(fileobj=compressed_file)
    with open("test_gzip", 'wb') as outfile:
        outfile.write(decompressed_file.read())

    x = 0
    while x < 10:
        yield {"x": x}
        x = x + 1
