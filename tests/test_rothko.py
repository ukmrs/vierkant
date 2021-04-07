import pytest
from src.ciphers.rothko import (calc_square_edge, Rothko, assemble_mod_square)
import numpy as np
from PIL import Image


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
    before_shuffle = shuffler.arr.copy()
    # get generators in sync as deshuffler
    # skips some steps
    for _ in range(shuffler.gens - deshuffler.gens):
        deshuffler.gen()
    assert deshuffler.gens == shuffler.gens

    # copy shuffled array, deshuffle it and compare to original
    shuffler.shuffle_squares()
    deshuffler.arr = shuffler.arr.copy()
    deshuffler.deshuffe_squares()
    assert (before_shuffle == deshuffler.arr).all()


def test_shuffle_deshuflle():
    shuffle_deshuffle_helper("simple", 'I enjoy Carly Rae Jepsen "Emotion"')
    shuffle_deshuffle_helper("longer\nkey2²©€½", 'ᖮᖯᖰᖱᖲᖳᖴᖵᖶᖷ')
    shuffle_deshuffle_helper("łə…yy",
                             ''.join(chr(i) for i in range(5000, 5400)))


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


def ed_mod_square_helper(appendix, key):
    r1, r2 = DbgRothko(key), DbgRothko(key)
    out = assemble_mod_square(r1.encode_mod_square(appendix))
    ex_appendix_key = r2.gen()
    a = r2.decode_mod_square(out, ex_appendix_key)

    assert r1.gens == r2.gens
    assert appendix == a


def test_encode_decode_mod_square():
    ed_mod_square_helper(10332, "a key of sorts")
    ed_mod_square_helper(0, "dfsfsdf 232")
    ed_mod_square_helper(1048547, "s1r431]\n\trf")
    ed_mod_square_helper(5, "s1r431rf")
    ed_mod_square_helper(5325, "dfsq")


# --- test encode decode ---

# whitespace, weird, simple and 256 bytes
KEYS = ("\t\n \t\n"
        "some\tthing\n eles Qqę2πśð„’ę©something", "simple key",
        "".join(chr(i) for i in range(200, 456)))


def ed_helper(original):  # ed feels unfortunate because of certain dysfunction
    for key in KEYS:
        encoded = Rothko(key).encode(original)
        assert original == Rothko(key).decode(encoded)


def test_ed_d():
    original = 'abcf'
    ed_helper(original)


def test_ed_weird():
    original = 'tes#^TEŋ ęß©t\n\tπś535ææœ ’æŋ’ðð’©ęþ'
    ed_helper(original)


def test_ed_simple():
    ed_helper("simple secret message")


def test_to_img_and_back():
    msg = "something interesting"
    r = Rothko("somekey")
    r.encode(msg)
    img = Image.fromarray(r.arr)
    r = Rothko("somekey").decode(np.asarray(img).copy())
    assert msg == r


@pytest.mark.slow
def test_ed_highunicode():
    """unicode characters except control/ASCII/Latin up to
    high surrogate weirdness"""
    ed_helper("".join(chr(i) for i in range(161, 55290)))
