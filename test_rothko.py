from rothko import (calc_square_edge, decode_mod_square, Rothko, insert_bits)
from itertools import cycle


def test_sq_edge():
    assert calc_square_edge(1) == 2
    assert calc_square_edge(9) == 2
    assert calc_square_edge(10) == 3
    assert calc_square_edge(24) == 3
    assert calc_square_edge(25) == 4


def test_decode_mod_square():
    assert decode_mod_square(1) == (1, 0)
    assert decode_mod_square(224) == (0, 56)
    assert decode_mod_square(34) == (2, 8)


def insert_helper(original, hashmap):
    out = insert_bits(original, hashmap)
    for k, v in hashmap.items():
        assert out[k] == v


def test_instert_bits():
    insert_helper(0b11111, {0: "1", 6: "0"})
    insert_helper(0b11111, {0: "0", 6: "0"})
    insert_helper(0b10001, {7: "0", 6: "1", 5: "0"})
    insert_helper(2555, {0: "1", 1: "0", 3: "1", 5: "0"})
    insert_helper(2**50, {k: v for k, v in zip(range(0, 53, 2), cycle('01'))})
