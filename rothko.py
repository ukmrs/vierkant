#!/usr/bin/env python3
from rc import RC4
import numpy as np
from math import ceil, sqrt
from PIL import Image


def calc_square_edge(encoded_len: int):
    pixel_amount = encoded_len / 3 + 1
    return ceil(sqrt(pixel_amount))


def create_pixel_array(encoded, edge: int, appendix: int):
    arr = np.asarray(encoded, dtype=np.uint8)
    arr = np.append(arr, np.random.randint(0, 256, appendix))
    arr.resize(edge, edge, 3)
    return arr


class Rothko():
    """creates colorful squares off given secret msg and key
    unless the user provided a dull msg :f """
    def __init__(self, key):
        self.rc = RC4(key)
        self.gen = self.xorshitf(sum(ord(c) for c in key) * len(key))

    def encode(self, secret):
        encoded = self.rc.encode(secret)
        remainder = len(encoded) % 3
        edge = calc_square_edge(len(encoded))
        appendix = edge**2 * 3 - len(encoded)
        arr = create_pixel_array(encoded, edge, appendix)
        print(encoded)
        print(arr)

    @staticmethod
    def xorshitf(seed: int):
        seed &= 0xFFFFFFFF
        while True:
            seed ^= np.left_shift(seed, 13)
            seed ^= np.right_shift(seed, 17)
            seed ^= np.left_shift(seed, 5)
            yield seed


if __name__ == "__main__":
    r = Rothko("dsfdf").encode("keufsdj")
