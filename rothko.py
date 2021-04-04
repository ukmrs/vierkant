#!/usr/bin/env python3
from rc import RC4
import numpy as np
from math import ceil, sqrt
from PIL import Image
from PIL.PngImagePlugin import PngImageFile, PngInfo
from collections import deque
from itertools import cycle


def binstrip(num: int):
    return bin(num)[2:]  # equivalent to .lstrip("0x")


def calc_square_edge(encoded_len: int):
    pixel_amount = encoded_len / 3 + 1
    return ceil(sqrt(pixel_amount))


def assemble_mod_square(bitseq: str):
    bitseq = bitseq.zfill(24)
    mod_square = np.zeros(3, dtype=np.uint8)
    for i in range(0, len(bitseq), 8):
        mod_square[i // 8] = int(bitseq[i:i + 8], 2)
    return mod_square


class Rothko():
    """creates colorful squares off given secret msg and key
    unless the user provided a dull msg :f"""

    max_shuffles = 250
    max_scale_up = 500
    temp_name = "picture.png"

    def __init__(self, key):
        self.rc = RC4(key)
        self.xor_gen = self.xorshitf(sum(ord(c) for c in key) * len(key))
        self.gen()
        self.arr = None

    def encode(self, secret):
        self.init_array(secret)
        self.shuffle_squares()
        dimension = int(sqrt(self.arr.shape[0]))
        self.arr.resize(dimension, dimension, 3)
        self.xor_gen.close()  # closing inf generator for peace of mind
        return self.arr

    def encode_to_img(self, secret, scale=False):
        self.encode(secret)
        edge, *_ = self.arr.shape
        if scale and (scale_up := (self.max_scale_up // edge)) > 1:
            s = edge * scale_up
            img = Image.fromarray(self.arr).resize((s, s), Image.NEAREST)
            meta = PngInfo()
            meta.add_text("edge", str(edge))
            img.save(self.temp_name, pnginfo=meta)
            return img
        return Image.fromarray(self.arr)

    def decode_from_img(self, image_path):
        img = PngImageFile(image_path)
        try:
            edge = img.text["edge"]
        except KeyError:
            pass
        else:
            edge = int(edge)
            img = img.resize((edge, edge), resample=Image.NEAREST)

        # asarray creates readonly hence the np.array
        return self.decode(np.array(img))

    def decode(self, arr):
        appendix_key = self.gen()
        self.gen()
        self.arr = arr
        dim = int(self.arr.shape[0]**2)
        self.arr.resize(dim, 3)
        self.deshuffe_squares()
        mod_square = self.arr[-1].copy()
        appendix = self.decode_mod_square(mod_square, appendix_key)
        self.arr.resize(dim * 3)
        self.xor_gen.close()
        return self.rc.decode(self.arr[:-appendix])

    def init_array(self, secret):
        encoded = np.asarray(self.rc.encode(secret), dtype=np.uint8)
        edge = calc_square_edge(len(encoded))
        appendix = edge**2 * 3 - len(encoded)
        mod_square = assemble_mod_square(self.encode_mod_square(appendix))
        self.arr = self.create_pixel_array(encoded, edge, appendix)
        self.arr[-1] = mod_square

    def create_pixel_array(self, encoded, edge: int, appendix: int):
        arr = np.asarray(encoded, dtype=np.uint8)
        # TODO make this deterministic with seeding
        seed = abs(self.gen())
        rng = np.random.default_rng(seed)
        arr = np.append(arr, rng.integers(0, 256, appendix, dtype=np.uint8))
        arr.resize(edge * edge, 3)
        return arr

    def encode_mod_square(self, appendix):
        encoded_appendix = (appendix ^ self.gen()) & 0xffffff
        return binstrip(encoded_appendix)

    @staticmethod
    def decode_mod_square(square, appendix_key) -> int:
        encoded = "".join(binstrip(byte).zfill(8) for byte in square)
        encoded = int(encoded, 2)
        return (encoded ^ appendix_key) & 0xffffff

    def calc_shuffling_amount(self, dim) -> int:
        amount = dim // 3 + 15
        return min(amount, self.max_shuffles)

    def __shuffle_core(self, dim, rng, shift, *args):
        """
        dim = amount of rows
        rng = function generating random numbers
        args = passed to range()
        shift = int 0 to 2
        """
        tmp = [True, True, True]
        tmp[shift] = False
        for i, row_time in zip(range(*args), cycle(tmp)):
            if row_time:  # swaps rows
                ix = i % dim
                rand = rng() % dim
                self.swap_arr_row(ix, rand)
            else:  # swaps columns
                ix = i % 3
                rand = rng() % 3
                self.swap_arr_column(ix, rand)

    def shuffle_squares(self):
        dim, *_ = self.arr.shape
        self.__shuffle_core(dim, self.gen, 2,
                            self.calc_shuffling_amount(dim) - 1, -1, -1)

    def deshuffe_squares(self):
        dim, *_ = self.arr.shape
        iterations = self.calc_shuffling_amount(dim)
        shift = iterations % 3
        swap_stack = deque(self.gen() for _ in range(iterations))
        self.__shuffle_core(dim, swap_stack.pop, shift, iterations)

    def swap_arr_row(self, i, j):
        self.arr[[i, j]] = self.arr[[j, i]]

    def swap_arr_column(self, i, j):
        self.arr[:, [i, j]] = self.arr[:, [j, i]]

    def gen(self):
        """convenience method that returns next xorshift gen yield"""
        return next(self.xor_gen)

    @staticmethod
    def xorshitf(seed: int):
        seed &= 0xffffffff
        while True:
            seed ^= np.left_shift(seed, 13)
            seed ^= np.right_shift(seed, 17)
            seed ^= np.left_shift(seed, 5)
            yield seed


if __name__ == "__main__":
    # msg = "".join(chr(i) for i in range(161, 55290))
    msg = "\n\tI am not happy\n\tand\n\tI am not sad\n"
    key = "krówka"
    img = Rothko(key).encode_to_img(msg, scale=True)
    # img.save("picture.png")

    scaled_down = img.resize((3, 3), Image.NEAREST)
    print(np.asarray(scaled_down))

    a = PngImageFile("picture.png")
    print(a.text)
    print(Rothko("key").decode_from_img("p2.png"))
