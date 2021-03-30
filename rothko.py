#!/usr/bin/env/ python3
"""This module contains the Rothko class which handles the encryption"""

# always to square


class Rothko():
    """Encryption class based on RC4A algorithm that also generates bitmaps?"""
    def __init__(self, key):
        self.sb = None  # statebox
        self.reset(key)  # looks akward but allows resetting the instance

    def encode(self, msg: str) -> str:
        """encodes"""
        return key

    def decode(self, msg: str) -> str:
        "decodes"
        return key

    def reset(self, key):
        """resets or initialiazes the class instance with a new key
        perform key scheduling algorithm"""
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

    def prgen(self, msg_len: int):
        "pseudo-random generation"
        s = self.sb  # mut ref for readability
        i, j = 0, 0
        for _ in range(msg_len):
            i = (i + 1) % 256
            j = (j + s[i]) % 256
            self.swap(i, j)
            a = (s[i] + s[j]) % 256
            b = (s[(i << 3 ^ j << 5) % 256] +
                 s[(i << 5 ^ j >> 3) % 256]) ^ 0xAA
            c = (j + s[j]) % 256
            yield (s[a] + s[b]) ^ c


if __name__ == "__main__":
    key = "hell\non\nearth#%@#%"
    inp = "I-am%not_happy(and_not_sad)"
    ro = Rothko(key)
    ro.encode(inp)
