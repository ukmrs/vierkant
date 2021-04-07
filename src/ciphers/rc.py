#!/usr/bin/env/ python3
"""This module contains the RC4 class which handles the encryption"""

from typing import List, Generator
# always to square


class RC4():
    """Encryption class based on RC4 algorithm that also generates bitmaps?"""
    def __init__(self, key):
        self.sb = None  # statebox
        self.reset(key)  # looks akward but allows resetting the instance

    def encode(self, msg: str):
        "API encode"
        return self._encode(bytearray(msg, encoding="utf8"))

    def _encode(self, ord_msg_gen) -> List[int]:
        """private encode"""
        pr_gen = self.prgen(len(ord_msg_gen))
        return [p ^ o for p, o in zip(pr_gen, ord_msg_gen)]

    def decode(self, msg: List[int]) -> str:
        return bytearray(self._encode(msg)).decode("utf8")

    def reset(self, key):
        """resets or initialiazes the class instance with a new key
        perform key scheduling algorithm"""
        # TODO if I care for utf8 above a byte then change this func
        key_len = len(key)  # len never changes
        j = 0
        self.sb = list(range(256))
        for i in range(256):
            j = (j + self.sb[i] + ord(key[i % key_len])) % 256
            self.swap(i, j)

    def swap(self, i, j):
        self.sb[i], self.sb[j] = self.sb[j], self.sb[i]

    def prgen(self, msg_len: int) -> Generator[int, None, None]:
        "pseudo-random generation"
        s = self.sb
        i, j = 0, 0
        for _ in range(msg_len):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            self.swap(i, j)
            yield s[(s[i] + s[j]) % 256]
