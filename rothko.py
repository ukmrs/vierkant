#!/usr/bin/env python3
from rc import RC4
import numpy as np
from math import ceil, sqrt
# from PIL import Image


class Rothko():
    """creates colorful squares off given secret msg and key
    unless the user provided a dull msg :f """
    def __init__(self, key):
        self.rc = RC4(key)

    def test(self, msg):
        encoded = self.rc.encode(msg)
        length = ((len(encoded) + 1) / 3)
        arr = np.asarray(encoded, dtype=np.uint8)

        dim = ceil(sqrt(length))
        appendix = dim**2*3 - arr.size
        arr = np.append(arr, np.random.randint(0, 256, appendix))
        arr.resize(dim, dim, 3)
        print(encoded)
        print(arr)

    def encode(self, secret):
        self.rc.encode(secret)

    @staticmethod
    def xorshitf(seed: int):
        seed ^= np.left_shift(seed, 13)
        seed ^= np.right_shift(seed, 17)
        seed ^= np.left_shift(seed, 5)
