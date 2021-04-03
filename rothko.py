#!/usr/bin/env python3
from rc import RC4
import numpy as np
import random
from math import ceil, sqrt
from PIL import Image
from typing import Tuple
from collections import deque


def binstrip(num: int):
    return bin(num)[2:]  # equivalent to .lstrip("0x")


def calc_square_edge(encoded_len: int):
    pixel_amount = encoded_len / 3 + 1
    return ceil(sqrt(pixel_amount))


def create_pixel_array(encoded, edge: int, appendix: int):
    arr = np.asarray(encoded, dtype=np.uint8)
    arr = np.append(arr, np.random.randint(0, 256, appendix))
    arr.resize(edge * edge, 3)
    return arr


def calc_encoded_ex_appendix(ex_appendix, xored):
    return ex_appendix ^ xored & 0x3fffff


def insert_bits(original: int, bits: dict):
    out = ""
    shift = 0
    for bl in binstrip(original).zfill(22):
        while shift in bits:
            out += bits[shift]
            shift += 1
        out += bl
        shift += 1
    while shift in bits:
        out += bits[shift]
        shift += 1
    return out


def assemble_mod_square(bitseq: str):
    mod_square = np.zeros(3, dtype=np.uint8)
    for i in range(0, len(bitseq), 8):
        mod_square[i // 8] = int(bitseq[i:i + 8], 2)
    return mod_square


class Rothko():
    """creates colorful squares off given secret msg and key
    unless the user provided a dull msg :f"""

    max_shuffles = 250

    def __init__(self, key):
        self.rc = RC4(key)
        self.xor_gen = self.xorshitf(sum(ord(c) for c in key) * len(key))
        self.gen()
        self.arr = None

    def encode(self, secret):
        encoded = np.asarray(self.rc.encode(secret), dtype=np.uint8)
        leftovers = len(encoded) % 3
        edge = calc_square_edge(len(encoded))
        appendix = edge**2 * 3 - len(encoded)
        ex_appendix = appendix - 1
        self.arr = create_pixel_array(encoded, edge, appendix)
        print(self.arr)
        mod_square = assemble_mod_square(
            self.encode_mod_square(ex_appendix, leftovers))

        self.shuffle_squares()
        print(self.arr)

    def init_array(self, secret):
        encoded = np.asarray(self.rc.encode(secret), dtype=np.uint8)
        leftovers = len(encoded) % 3
        edge = calc_square_edge(len(encoded))
        appendix = edge**2 * 3 - len(encoded)
        ex_appendix = appendix - 1
        self.arr = create_pixel_array(encoded, edge, appendix)
        mod_square = assemble_mod_square(
            self.encode_mod_square(ex_appendix, leftovers))
        self.arr[-1] = mod_square

    def decode(self, arr):
        self.arr = arr
        self.gen()
        self.gen()
        self.gen()
        self.deshuffe_squares()

    def encode_mod_square(self, ex_appendix, leftovers):
        """Prepares and encodes information in the mod square
        about the amount of non-significant random squares
        called here ex_appendix and the amount of leftovers"""

        lin = binstrip(leftovers).zfill(2) if leftovers else random.choice(
            ("00", "11"))
        first, second = self.calc_mod_bits_positions()
        encoded_ex_appendix = (ex_appendix ^ self.gen()) & 0x3fffff
        bitseq = insert_bits(encoded_ex_appendix, {
            first: lin[0],
            second: lin[1]
        })
        return bitseq

    def decode_mod_square(self, square, first_bit_pos,
                          second_bit_pos) -> Tuple[int, int]:
        # TODO change it is so its not hacky
        # shifts and masks for instance
        bits = list("".join(binstrip(byte).zfill(8) for byte in square))

        if first_bit_pos > second_bit_pos:
            first_bit = bits.pop(first_bit_pos)
            second_bit = bits.pop(second_bit_pos)
        else:
            second_bit = bits.pop(second_bit_pos)
            first_bit = bits.pop(first_bit_pos)

        leftovers = int((first_bit + second_bit), 2) % 3  # 11 and 00 both 0
        encoded = int("".join(bits), 2)

        decoded_ex_appendix = (encoded ^ self.gen()) & 0x3fffff

        return leftovers, decoded_ex_appendix

    def calc_shuffling_amount(self, dim) -> int:
        return min(dim // 3 + 2, self.max_shuffles)

    def shuffle_squares(self):
        dim, *_ = self.arr.shape
        for i in range(self.calc_shuffling_amount(dim) - 1, -1, -1):
            ix = i % dim
            rand = self.gen() % dim
            print(ix, rand)
            self.swap_arr(ix, rand)
        print(self.arr)

    def deshuffe_squares(self):
        dim, *_ = self.arr.shape
        iterations = self.calc_shuffling_amount(dim)
        swap_stack = deque(self.gen() % dim for _ in range(iterations))
        for i in range(iterations):
            ix = i % dim
            rand = swap_stack.pop()
            print(ix, rand)
            self.swap_arr(ix, rand)
        print("deshuffled\n", self.arr)

    def swap_arr(self, i, j):
        # usual python swapping doesnt work with numpy views
        tmp = np.copy(self.arr[i])
        self.arr[i] = self.arr[j]
        self.arr[j] = tmp

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

    @staticmethod
    def xorshitf(seed: int):
        seed &= 0xFFFFFFFF
        while True:
            seed ^= np.left_shift(seed, 13)
            seed ^= np.right_shift(seed, 17)
            seed ^= np.left_shift(seed, 5)
            yield seed


if __name__ == "__main__":

    class DbgRothko(Rothko):
        def __init__(self, *args, **kwargs):
            self.gens = 0
            super().__init__(*args, **kwargs)

        def gen(self):
            self.gens += 1
            return super().gen()

    r = DbgRothko("simple key")
    out = r.init_array("msgæəð→ə„")
    before_shuffle = r.arr

    r2 = DbgRothko("simple key")
    for i in range(r.gens - r2.gens):
        r2.gen()
    assert r2.gens == r.gens
    r.shuffle_squares()
    r2.arr = r.arr.copy()
    r2.deshuffe_squares()
    assert (before_shuffle == r2.arr).copy
