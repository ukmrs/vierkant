#!/usr/bin/env/ python3
"""This module contains the Rothko class which handles the encryption"""


class Rothko():
    """Encryption class based on RC4A algorithm that also generates bitmaps?"""
    statebox = list(range(256))

    def encode(self, key: str) -> str:
        """encodes"""
        return key

    def deconde(self, key: str) -> str:
        "decodes"
        return key

    def swap(self, i, j):
        self.statebox[i], self.statebox[j] = self.statebox[j], self.statebox[i]
