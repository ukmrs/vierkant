from rothko import (calc_square_edge, Rothko, insert_bits, assemble_mod_square)
from itertools import cycle
import numpy as np


class DbgRothko(Rothko):
    def __init__(self, *args, **kwargs):
        self.gens = 0
        super().__init__(*args, **kwargs)

    def gen(self):
        self.gens += 1
        return super().gen()


def shuffle_deshuffle_helper(key, secret):
    shuffler, deshuffler = DbgRothko(key), DbgRothko(key)
    shuffler.init_array(secret)
    before_shuffle = shuffler.arr
    # get generators in sync as deshuffler
    # skips some steps
    for _ in range(shuffler.gens - deshuffler.gens):
        deshuffler.gen()
    assert deshuffler.gens == shuffler.gens

    # copy shuffled array, deshuffle it and compare to original
    shuffler.shuffle_squares()
    deshuffler.arr = shuffler.arr.copy()
    deshuffler.deshuffe_squares()
    assert (before_shuffle == deshuffler.arr).copy


def test_shuffle_deshuflle():
    shuffle_deshuffle_helper("simple", 'I enjoy Carly Rae Jepsen "Emotion"')
    shuffle_deshuffle_helper("longer\nkey2²©€½", 'ᖮᖯᖰᖱᖲᖳᖴᖵᖶᖷ')
    shuffle_deshuffle_helper("łə…yy",
                             ''.join(chr(i) for i in range(5000, 5400)))


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


def test_sq_edge():
    assert calc_square_edge(1) == 2
    assert calc_square_edge(9) == 2
    assert calc_square_edge(10) == 3
    assert calc_square_edge(24) == 3
    assert calc_square_edge(25) == 4


def test_assemble_mod_square():
    out = assemble_mod_square("110010000010110000000000")
    mx = assemble_mod_square("".join("1" for _ in range(24)))
    mn = assemble_mod_square("".join("0" for _ in range(24)))
    assert (out == np.array([200, 44, 0])).all()  # type: ignore
    assert (mx == np.array([255, 255, 255])).all()  # type: ignore
    assert (mn == np.array([0, 0, 0])).all()  # type: ignore


def encode_decode_helper(appendix, leftovers, key):
    r1, r2 = Rothko(key), Rothko(key)
    out = assemble_mod_square(r1.encode_mod_square(appendix, leftovers))
    pos1, pos2 = r2.calc_mod_bits_positions()
    lft, a = r2.decode_mod_square(out, pos1, pos2)

    assert r1.gen() == r2.gen()
    assert appendix == a
    assert lft == leftovers


def test_encode_decode_mod_square():
    encode_decode_helper(10332, 2, "a key of sorts")
    encode_decode_helper(0, 1, "dfsfsdf 232")
    encode_decode_helper(1048547, 2, "s1r431]\n\trf")
    encode_decode_helper(5, 0, "s1r431rf")
    encode_decode_helper(5325, 1, "dfsq")
