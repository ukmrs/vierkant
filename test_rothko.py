from rothko import Rothko
from collections import namedtuple

RC4example = namedtuple('RC4example',
                        ['key', 'keystream', 'input', 'Ciphertext'])

one = RC4example('Key', 'EB9F7781B734CA72A719', 'plaintext',
                 'BBF316E8D940AF0AD3')


def test_rothko_against_examples():
    pass


def test_rothko_encode_decode():
    inp = 'tes#^TEŋęß©t\n\tπśææœ’æŋ’ðð’©ęþ'
    key = "some\tthing\n eles Qqęπśð„’ę©"
    out = Rothko(key).decode(Rothko(key).encode(inp))
    assert inp == out
