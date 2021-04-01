#!/usr/bin/env/ python3
"""This module contains the Rothko class which handles the encryption"""

from typing import Iterator, List
# always to square


class RC4():
    """Encryption class based on RC4A algorithm that also generates bitmaps?"""
    def __init__(self, key):
        self.sb = None  # statebox
        self.reset(key)  # looks akward but allows resetting the instance

    def encode(self, msg: str):
        "API encode"
        return self._encode([ord(char) for char in msg])

    def _encode(self, ord_msg_gen: List[int]) -> List[int]:
        """private encode"""
        pr_gen = self.prgen(len(ord_msg_gen))
        return [p ^ o for p, o in zip(pr_gen, ord_msg_gen)]

    def decode(self, msg: List[int]) -> str:
        return "".join((chr(c) for c in self._encode(msg)))

    def reset(self, key):
        """resets or initialiazes the class instance with a new key
        perform key scheduling algorithm"""
        key_len = len(key)  # len never changes
        j = 0
        self.sb = list(range(256))
        for i in range(256):
            j = (j + self.sb[i] + ord(key[i % key_len])) % 256
            self.swap(i, j)

    def swap(self, i, j):
        self.sb[i], self.sb[j] = self.sb[j], self.sb[i]

    def prgen(self, msg_len: int) -> Iterator[int]:
        "pseudo-random generation"
        s = self.sb
        i, j = 0, 0
        for _ in range(msg_len):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            self.swap(i, j)
            yield s[(s[i] + s[j]) % 256]
