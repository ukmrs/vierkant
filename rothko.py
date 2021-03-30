#!/usr/bin/env/ python3
"""This module contains the Rothko class which handles the encryption"""


class Rothko():
    """Encryption class based on RC4A algorithm that also generates bitmaps?"""
    def __init__(self, key):
        self.sb = None  # statebox
        self._reset(key)  # looks akward but allows resetting the instance

    def encode(self, key: str) -> str:
        """encodes"""
        return key

    def decode(self, key: str) -> str:
        "decodes"
        return key

    def _reset(self, key):
        """resets or initialiazes the class instance with a new key"""
        key_len = len(key)  # len never changes
        # accesing var is faster than calling len
        # doesn't necesserily matter with only 256 calls but hey
        j = 0
        self.sb = list(range(256))
        for i in range(256):
            j = (j + self.sb[i] + ord(key[i % key_len])) % 256
            self.swap(i, j)

    def swap(self, i, j):
        self.sb[i], self.sb[j] = self.sb[j], self.sb[i]
