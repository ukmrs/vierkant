#!/usr/bin/env python3
from rc import RC4
import numpy as np
import random
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


def decode_mod_square(square):
    """decodes info about how many leftovers they were in the last square
    [significant, random, random] -> 2 etc
    checks if it encodes info about amount of random values"""
    leftovers = (square & 3) % 3
    div = square >> 2
    return leftovers, div


def calc_encoded_ex_appendix(ex_appendix, xored):
    return ex_appendix ^ xored & 0x3fffff


def insert_bits(original: int, bits: dict):
    out = ""
    shift = 0
    for bl in bin(original).lstrip("0b"):
        while shift in bits:
            out += bits[shift]
            shift += 1
        out += bl
        shift += 1
    while shift in bits:
        out += bits[shift]
        shift += 1
    return out


class Rothko():
    """creates colorful squares off given secret msg and key
    unless the user provided a dull msg :f """
    def __init__(self, key):
        self.rc = RC4(key)
        self.xor_gen = self.xorshitf(sum(ord(c) for c in key) * len(key))
        self.gen()
        self.arr = None

    def encode(self, secret):
        encoded = np.asarray(self.rc.encode(secret), dtype=np.uint8)
        remainder = len(encoded) % 3
        edge = calc_square_edge(len(encoded))
        appendix = edge**2 * 3 - len(encoded)
        self.arr = create_pixel_array(encoded, edge, appendix)

        mod_square_position = self.gen() % edge**2

    def assemble_mod_square(self, ex_appendix):
        """Prepares and encodes information in the mod square
        about the amount of non-significant random squares
        called here ex_appendix and the amount of leftovers"""
        first, second = self.calc_mod_bits_positions()
        tmp = ex_appendix ^ self.gen() & 0x3fffff

    def calc_mod_bits_positions(self):
        """return position of bits in the mod_square that hold
        information about leftovers. the mod square is 3bytes
        so there are 24 positions for bits"""
        first_bit = self.gen() % 24
        second_bit = self.gen() % 24
        if second_bit == first_bit:
            second_bit = (first_bit + 1 % 24)
        return first_bit, second_bit

    def gen(self):
        """just a conviencince methods that return next xorshift gen yield"""
        return next(self.xor_gen)

    def encode_mod_square(self, appendix):
        appendix -= 1  # excluding mod square which is a part of appendix
        first_bit = self.gen() % 24  # 3*8 bits to choose from
        second_bit = self.gen() % 24
        if second_bit == first_bit:  #  make sure bits are distinct
            second_bit = (first_bit + 1 % 24)
        div = self.gen() % 24

    @staticmethod
    def xorshitf(seed: int):
        seed &= 0xFFFFFFFF
        while True:
            seed ^= np.left_shift(seed, 13)
            seed ^= np.right_shift(seed, 17)
            seed ^= np.left_shift(seed, 5)
            yield seed


if __name__ == "__main__":
    r = Rothko("dsfdsdfsdf").encode("keuffwe23fwfsdj")
