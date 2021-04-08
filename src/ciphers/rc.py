from typing import List, Generator
import numpy as np
# always to square


class RC4():
    """RC4 stream cipher
    basic usage:
    ```
    key, msg = "key", "message"
    encoded = RC4(key).encode(msg)
    decoded = RC4(key).decode(encoded)
    ```
    key scheduling and pseudo random generation algorithm are implemented
    as described here:
    Klein, A. Attacks on the RC4 stream cipher.
    Des. Codes Cryptogr. 48, 269–286 (2008)."""
    def __init__(self, key):
        self.sb = None  # statebox
        # performs key scheduling, can be called again to reset the instance
        self.ksa(key)

    def encode(self, msg: str) -> List[int]:
        """encodes given msg and returns list of ints within uint8 range
        representing bytes"""
        return self._encode(bytearray(msg, encoding="utf8"))

    def _encode(self, msg_bytes) -> List[int]:
        """private encode"""
        pr_gen = self.prgen(len(msg_bytes))
        return [p ^ o for p, o in zip(pr_gen, msg_bytes)]

    def decode(self, msg: List[int]) -> str:
        """expects list of ints representing bytes and decodes
        the message"""
        try:
            return bytearray(self._encode(msg)).decode("utf8")
        except UnicodeDecodeError:
            # secret decoded with a wrong key can produce invalid utf8 bytes
            return ""

    def ksa(self, key) -> None:
        """key scheduling algorithm, generates initial permutation"""
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
